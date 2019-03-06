# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:34:47 2019

@author: neilw
"""
from operator import add
from discountfactor import discountfactor

def fixedloanrepayment(borrowing,interest,length,staggerpart,cost_freight,discount):
    
    """calculates repayment of loan and interest in fixed installments"""
    borrowingpart = borrowing/staggerpart+(staggerpart-1)*cost_freight
    fixedloanrepayment = borrowingpart*interest/(1-(1+interest)**-length)
    loanschedule=[fixedloanrepayment]*length
    for i in range(len(loanschedule)):
        loanschedule[i]=loanschedule[i]*discountfactor(discount,0,i)
    

    totalduration = length+staggerpart-1
    loanrepaymentschedule = [0]*totalduration
    for i in range(staggerpart):
        temp1=[0]*i+loanschedule+[0]*(totalduration-length-i)
        loanrepaymentschedule=list(map(add,loanrepaymentschedule,temp1))
        
    
    return loanrepaymentschedule
