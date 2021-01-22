/*
* @file botTemplate.cpp
* @author Arun Tejasvi Chaganty <arunchaganty@gmail.com>
* @date 2010-02-04
* Template for users to create their own bots
*/

#include "Othello.h"
#include "OthelloBoard.h"
#include "OthelloPlayer.h"
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <list> 
#include <iterator> 
#include <cmath>
#include <climits>
#include <time.h>
using namespace std;
using namespace Desdemona;

class Res
{
    public:
    Move mv=Move(0,0);
    int value;
    
};

class MyBot: public OthelloPlayer
{
    public:
        /**
         * Initialisation routines here
         * This could do anything from open up a cache of "best moves" to
         * spawning a background processing thread. 
         */
        MyBot( Turn turn );

        /**
         * Play something 
         */
        virtual Move play( const OthelloBoard& board );
        Res minimax(Turn turn,int depth,const OthelloBoard& board,Turn turn1);
        bool isEven(int n);
    private:
};

MyBot::MyBot( Turn turn )
    : OthelloPlayer( turn )
{
}
bool MyBot::isEven(int n)
{
	if(n%2==0)
		return true;
	else
		return false;
}

Move MyBot::play( const OthelloBoard& board )
{
    list<Move> moves = board.getValidMoves( turn );
    //int randNo = rand() % moves.size();
    if(moves.size()==0)
    { Move m(2,3);
      m.x=-1;
      m.y=-1;
      return m;
    }
    else
    {
        
      
       return minimax(turn,0,board,turn).mv;
    }
    //list<Move>::iterator it = moves.begin();
    //return *it;
}

Res MyBot::minimax(Turn turn,int depth,const OthelloBoard& board,Turn turn1)
{
    if(depth==4)
    {
         if( turn1==BLACK )
         {
             Res r;
             r.value=board.getBlackCount()-board.getRedCount();
                return r;
         }
         else
         {
         	 Res r;
             r.value=-board.getBlackCount()+board.getRedCount();
                return r;
         }
        
    }
    else 
    {
        list<Move> moves = board.getValidMoves( turn );
        list<Move>::iterator it;
        if( moves.size()!=0)
        {
          int j=0;
          int cvj=-1;
          Res r;
          r.value=cvj;
         for(it=moves.begin();it!=moves.end();++it)
         {
            OthelloBoard tempBoard=OthelloBoard(board);
            tempBoard.makeMove(turn,*it);
            j++;
            int temp=minimax(other(turn),depth+1,tempBoard,turn1).value;
            if(j==1)
            {
            	r.mv=*it;
            	r.value=temp;
            	cvj=temp;
            }
            else
            {
            if(turn==turn1)
            {
              if(temp>cvj)
               {
                  cvj=temp;
                  r.value=cvj;
                  r.mv=*it;   
               }
            }
            else
            {
            	if(temp<cvj)
                {
                  cvj=temp;
                  r.value=cvj;
                  r.mv=*it;   
                }
            }
           
            }

         }
         return r;
        }
        else
        {
            moves = board.getValidMoves(other(turn) );
            if(moves.size()==0)
            {
                   if( turn1==BLACK )
                   {
                         Res r;
                         r.value=board.getBlackCount()-board.getRedCount();
                         return r;
                   }
                   else
                   {
         	          Res r;
                      r.value=-board.getBlackCount()+board.getRedCount();
                      return r;
                   }
            }
            else
            {
                int j=0;
          int cvj=-1;
          Res r;
          r.value=cvj;
         for(it=moves.begin();it!=moves.end();++it)
         {
            OthelloBoard tempBoard=OthelloBoard(board);
            tempBoard.makeMove(other(turn),*it);
            j++;
            int temp=minimax(turn,depth,tempBoard,turn1).value;
            if(j==1)
            {
            	r.mv=*it;
            	r.value=temp;
            	cvj=temp;
            }
            else
            {
               if(other(turn)==turn1)
               {
                 if(temp>cvj)
                 {
                  cvj=temp;
                  r.value=cvj;
                  r.mv=*it;   
                 }
               }
               else
               {
            	if(temp<cvj)
                {
                  cvj=temp;
                  r.value=cvj;
                  r.mv=*it;   
                }
               }
           
            } 
          }
            return r;
        }
        
    }
   
 }
}


// The following lines are _very_ important to create a bot module for Desdemona

extern "C" {
    OthelloPlayer* createBot( Turn turn )
    {
        return new MyBot( turn );
    }

    void destroyBot( OthelloPlayer* bot )
    {
        delete bot;
    }
}


