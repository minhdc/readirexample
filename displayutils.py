def printProgressBar(iteration,total,prefix='',suffix='',decimals = 1, length = 100,fill='█'):
    '''
        @params:
            iter    - R - current iteration
            total   - R - total iterations
            prefix  - O - prefix string
            suffix  - O - suffix string
            decimals- O - positive number of dec in percent complete
            length  - O - character length of bar
            fill    - O - bar fill character
    '''
    
    percent = 0
    filledLength = 0
    try:
        percent = ("{0:."+str(decimals) + "f}").format(100 * (iteration/float(total)))
        filledLength = int(length * iteration // total)
    except ZeroDivisionError:
        print()
        #return
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s'%(prefix,bar,percent,suffix), end = '\r')

    if iteration == total:
        print()