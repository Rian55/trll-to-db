from trello import TrelloClient
import apiKeys as k
import Board
import Task
from firebase_admin import initialize_app
from firebase_admin import credentials
from google.cloud import firestore
import os
from datetime import datetime



def toLog(text):
    file = open('logs.txt', 'a+')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string,": ",text, file = file)
    file.close()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = k.path_to_GAC
CREDENTIALS = credentials.Certificate(k.path_to_certificate)
initialize_app(CREDENTIALS)
FIRESTORE = firestore.Client()

CLIENT = TrelloClient(
    api_key = k.api_key,
    api_secret = k.api_secret,
    token = k.token,
    #token_secret = 'your-oauth-token-secret'
)

organizations = []
ALL_BOARDS = []
ALL_MEMBERS = []

try:
    organizations = CLIENT.list_organizations()
    EWP_ORGANIZATION = organizations[0]

    for org in organizations:
        if org.name == "ewpteam":
            EWP_ORGANIZATION = org

    ALL_BOARDS = EWP_ORGANIZATION.get_boards(list_filter = "open")
    ALL_MEMBERS = EWP_ORGANIZATION.get_members()
    toLog("Succesfully getting organizations/boards/members")
except:
    toLog("Error getting organizations/boards/members")

def set_update_boards(boards):
    boards_to_send = []

    for board in boards:
        members = []
        for member in board.all_members():
            members.append(member.full_name)
        lists = []
        for list in board.get_lists(list_filter = "open"):
            lists.append(list.name)
        new_board = Board.Board(id = board.id, name = board.name, members = members, lists = lists)
        boards_to_send.append(new_board)

    toLog("Board list has been succesfully created.")
    boards_ref = FIRESTORE.collection(u'boards')

    for board in boards_to_send:
        boards_ref.document(board.id).set(board.to_dict(), merge = True)

    toLog("Board list has been succesfully pushed to firestore.")

try:
    set_update_boards(ALL_BOARDS)
except:
    toLog("Error in set_update_boards")


def set_update_tasks(boards):
    tasks_to_send = []

    for board in boards:

        for task in board.get_cards(card_filter = "open"):
            members = []
            for memID in task.idMembers:
                for mem in ALL_MEMBERS:
                    if memID == mem.id:
                        members.append(mem.full_name)

            tasks_to_send.append(Task.Task(id = task.id, title = task.name, list = task.get_list().name,\
                                           createdDate = task.created_date, board = board.name,\
                                           members = members, dueDate = task.due_date))

    toLog("Task list has been succesfully created.")
    tasks_ref = FIRESTORE.collection(u'tasks')

    for task in tasks_to_send:
        tasks_ref.document(task.id).set(task.to_dict(), merge = True)

    toLog("Task list has been succesfully pushed to firestore.")

try:
    set_update_tasks(ALL_BOARDS)
except:
    toLog("Error in set_update_tasks.")
