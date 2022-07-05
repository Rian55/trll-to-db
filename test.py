from trello import TrelloClient
import apiKeys as k

client = TrelloClient(
    api_key=k.api_key,
    api_secret=k.api_secret,
    token=k.token,
    #token_secret='your-oauth-token-secret'
)

all_boards = client.list_boards()
HGD_BOARD = all_boards[0]
for board in all_boards:
    if board.name == "Haftalık Görev Dağılımı":
        HGD_BOARD = board

print(HGD_BOARD.name)
members = HGD_BOARD.all_members()
for member in members:
    print(member.full_name)
