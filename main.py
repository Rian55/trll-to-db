#!/usr/bin/env python3
from time import sleep
from trello import TrelloClient
import apiKeys as Key
import Board
import Task
from firebase_admin import initialize_app
from firebase_admin import credentials
from google.cloud import firestore
import os
from datetime import datetime

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
    boards_ref = FIRESTORE.collection(u'boards')

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

            tasks_to_send.append(Task.Task(id=task.id, title=task.name, list=task.get_list().name,
                                           createdDate=task.created_date, board=board.name, members=members,
                                           dueDate=task.due_date))

    to_log("Task list has been successfully created.")

    for task in tasks_to_send:
        tasks_ref.document(task.id).set(task.to_dict(), merge=True)

    to_log("Task list has been successfully pushed to firestore.")


def write_to_fb():
    global ALL_BOARDS
    try:
        organizations = CLIENT.list_organizations()
        EWP_ORGANIZATION = organizations[0]

        for org in organizations:
            if org.name == "ewpteam":
                EWP_ORGANIZATION = org

        ALL_BOARDS = EWP_ORGANIZATION.get_boards(list_filter="open")
        ALL_MEMBERS = EWP_ORGANIZATION.get_members()
        to_log("Successfully getting organizations/boards/members")
    except:
        to_log("Error getting organizations/boards/members")

    try:
        set_update_boards(ALL_BOARDS)
    except:
        to_log("Error in set_update_boards")

    try:
        set_update_tasks(ALL_BOARDS)
    except:
        to_log("Error in set_update_tasks.")


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New city: {change.document.id}')
        elif change.type.name == 'MODIFIED':
            CLIENT.get_card(change.document.id).name.set_closed(True)

write_to_fb()
query_watch = tasks_ref.on_snapshot(on_snapshot)
while True:
    sleep(1)
