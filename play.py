from boardConvert import *
import chess
from keras.models import load_model
from time import sleep
#from IPython.display import display, HTML, clear_output
import chess.engine
import keras

engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
model = load_model("test2.h5")
board = chess.Board()


def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(alpha, beta):
    stand_pat = model_evaluate(board)
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


def selectmove(depth):
    bestMove = chess.Move.null()
    bestValue = -9
    alpha = -10
    beta = 10
    for move in board.legal_moves:
        board.push(move)
        boardValue = -alphabeta(-beta, -alpha, depth - 1)
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move
        if (boardValue > alpha):
            alpha = boardValue
        board.pop()
    return bestMove


def model_evaluate(board):
    matrix = make_matrix(board)
    trans_input = translate(matrix, chess_dict)
    eval_score = model.predict(trans_input.reshape(1, 8, 8, 12), verbose=0)
    return eval_score


def display_board(board, use_svg):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"


print('program ready')
moves = []
pgn = ''
counter = 1
for i in range(100):
    if board.turn == chess.BLACK:
        print("engine to move")
        move = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(move.move)


    else:
        move = selectmove(2)
        string = str(board.san(move)) + ' '
        pgn += string
        moves.append(board.san(move))
        board.push(move)
        print("move_made")

    print(board)

    #clear_output(wait=True)
    #display(HTML(html))

    if board.is_game_over():
        break