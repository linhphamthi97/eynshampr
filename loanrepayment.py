# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:34:47 2019

@author: neilw
"""

def fixedloanrepayment(borrowing,interest,length):
    """calculates repayment of loan and interest in fixed installments"""
    fixedloanrepayment = borrowing*interest/(1-(1+interest)^-length)
    return fixedloanrepayment
