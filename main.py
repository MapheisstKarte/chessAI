import time

import chess

import AI

board = chess.Board()
move_finder = AI.MoveFinder(board)

print(board)

# app = flask.Flask(__name__)
# ^
#
# @app.route("/board", methods=["GET", "POST"])
# def interact_with_chess() -> Response:
#     if request.method == "GET":
#         return Response(str(board))
#     elif request.method == "POST":
#         move = request.data.decode("utf8")
#         board.push_san(move)
#         return Response(str(board))
#
# @app.route("/legalmoves", methods=["GET"])
# def get_legal_moves() -> Response:
#     legal_moves = [str(move) for move in board.legal_moves]
#     return app.response_class(
#         response=json.dumps(legal_moves),
#         status=200,
#         mimetype="application/json"
#     )
#
#
# app.run("localhost", 80)

while not board.is_game_over():

    if board.turn:

        playerMove = input()
        board.push_san(playerMove)
        timeStart = time.time()
        print(board)

    elif not board.turn:

        print("-------------------------------")
        AIMove = move_finder.findBestMoveNegaMax(board)
        board.push(AIMove)

        print("nodes per second: " + str(round(move_finder.counter / (time.time() - timeStart))) + "\n"
              + "Time to move: " + str(time.time() - timeStart))

        evaluation = AI.evaluate(board)
        print("Evaluation " + str(evaluation))
        print("AI Move: " + chess.Move.__str__(AIMove))
        print(board)
        print("-------------------------------")

else:

    print("Game Over: " + board.result())
