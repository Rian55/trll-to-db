#!/usr/bin/env python3
from time import sleep
from trello import TrelloClient
from dateutil import parser
import apiKeys as Key
import Board
import Task
from firebase_admin import initialize_app
from firebase_admin import credentials
from google.cloud import firestore
import os
from datetime import datetime
import schedule

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Key.path_to_GAC
CREDENTIALS = credentials.Certificate(Key.path_to_certificate)
initialize_app(CREDENTIALS)
FIRESTORE = firestore.Client()

CLIENT = TrelloClient(
    api_key=Key.api_key,
    api_secret=Key.api_secret,
    token=Key.token,
    # token_secret = 'your-oauth-token-secret'
)

organizations = []
ALL_BOARDS = []
ALL_MEMBERS = []
tasks_ref = FIRESTORE.collection(u'tasks')
boards_ref = FIRESTORE.collection(u'boards')


def to_log(text):
    file = open('logs.txt', 'a+')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string, ": ", text, file=file)
    file.close()


def set_update_boards(boards):
    boards_to_send = []

    for board in boards:
        members = []
        for member in board.all_members():
            members.append(member.full_name)
        lists = []
        for trelloList in board.get_lists(list_filter="open"):
            lists.append(trelloList.name)
        new_board = Board.Board(id=board.id, name=board.name, members=members, lists=lists)
        boards_to_send.append(new_board)

    to_log("Board list has been successfully created.")

    for board in boards_to_send:
        boards_ref.document(board.id).set(board.to_dict(), merge=True)

    to_log("Board list has been successfully pushed to firestore.")


def set_update_tasks(boards):
    tasks_to_send = []

    for board in boards:

        for task in board.get_cards(card_filter="open"):
            members = []
            for memID in task.idMembers:
                for mem in ALL_MEMBERS:
                    if memID == mem.id:
                        members.append(mem.full_name)

            dueDate = task.due_date
            if dueDate == "":
                dueDate = datetime(1, 1, 1, 0, 0)
            tasks_to_send.append(Task.Task(id=task.id, title=task.name, list=task.get_list().name,
                                           createdDate=task.created_date, board=board.name, members=members,
                                           dueDate=dueDate))

    to_log("Task list has been successfully created.")

    for task in tasks_to_send:
        tasks_ref.document(task.id).set(task.to_dict(), merge=True)

    to_log("Task list has been successfully pushed to firestore.")


def write_to_fb():
    global ALL_BOARDS
    global ALL_MEMBERS
    try:
        organizations = CLIENT.list_organizations()
        EWP_ORGANIZATION = organizations[0]

        for org in organizations:
            if org.name == "ewpteam":
                EWP_ORGANIZATION = org

        ALL_BOARDS = EWP_ORGANIZATION.get_boards(list_filter="open")
        ALL_MEMBERS = EWP_ORGANIZATION.get_members()
        to_log("Successfully getting organizations/boards/members")
    except Exception as e:
        print(e)
        to_log("Error getting organizations/boards/members")

    try:
        set_update_boards(ALL_BOARDS)
    except Exception as e:
        print(e)
        to_log("Error in set_update_boards")

    try:
        set_update_tasks(ALL_BOARDS)
    except Exception as e:
        print(e)
        to_log("Error in set_update_tasks.")


def add_task_to_trello(task: Task):
    task_list = None

    for board in ALL_BOARDS:
        if board.name == task.board:
            for trello_list in board.get_lists("open"):
                if trello_list.name == task.list:
                    task_list = trello_list

    if task_list is not None:
        new_task = task_list.add_card(name=task.title)
        for member in task.members:
            for org_member in ALL_MEMBERS:
                if member == org_member.full_name:
                    new_task.assign(org_member.id)
        new_task.set_due(parser.parse(task.dueDate))
        return new_task


CARD_ADDED_COUNT = 0


def on_snapshot(col_snapshot, changes, read_time):
    global CARD_ADDED_COUNT
    change_is_added = False

    for change in changes:
        doc_ref = tasks_ref.document(change.document.id).get()
        new_task = Task.Task(0, "", [""], datetime.now(), "")
        new_task.from_snapshot(snapshot=doc_ref)
        print(f"worked {change.document.id}")

        if change.type.name == 'ADDED':
            if len(change.document.id) != 24:
                trello_task = add_task_to_trello(new_task)
                new_task.id = trello_task.id
                tasks_ref.document(new_task.id).set(new_task.to_dict(), merge=True)
                tasks_ref.document(change.document.id).delete()
            change_is_added = True
        elif change.type.name == 'MODIFIED':
            if new_task.removed is True:
                CLIENT.get_card(change.document.id).set_closed(True)
    if change_is_added is True:
        CARD_ADDED_COUNT += 1

write_to_fb()
schedule.every(20).minutes.do(write_to_fb)
query_watch = tasks_ref.on_snapshot(on_snapshot)
while True:
    schedule.run_pending()
    sleep(1)
