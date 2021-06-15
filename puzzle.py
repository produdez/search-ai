# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import search
import random
import util

#! Puzzle State Class
class PuzzleState:
    """
    This class is the abstract class of any puzzle state
    """

    def __init__( self, *arg ):
        """
        Data structure of the puzzle is defined here
        """
        util.raiseNotDefined()

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.
          Boolean
        """
        util.raiseNotDefined()

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.
        """
        util.raiseNotDefined()

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        util.raiseNotDefined()

    # Utilities for comparison and display
    def __eq__(self, other):
        util.raiseNotDefined()

    def __hash__(self):
        util.raiseNotDefined()
    def __getAsciiString(self):
        """
          Returns a display string for the puzzle
        """
        util.raiseNotDefined()

    def __str__(self):
        return self.__getAsciiString()


