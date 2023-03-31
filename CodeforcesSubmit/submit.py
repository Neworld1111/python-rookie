from robobrowser import RoboBrowser
import getpass
import os
import time


CF_USER = {
    'handle': 'YourHandle', 'password': 'YourPasswd'
}

def main():

    # 登录

    print("Your Handle:",end='')
    CF_USER['handle'] = input()
    CF_USER['password'] = getpass.getpass(prompt='PassWord:')

    rb = RoboBrowser(parser='html.parser')
    rb.open('https://codeforces.com/enter')
    login_form = rb.get_form('enterForm')

    login_form['handleOrEmail'] = CF_USER['handle']
    login_form['password'] = CF_USER['password']
    rb.submit_form(login_form)

    # 验证是否登录成功
    try:
        userName = rb.find('div',class_='for-avatar') #.find('a').get('href')
        if str(userName) != 'None':
            os.system('clear')
            userName = str(userName.find('a').get('href'))
            print('\033[0;37;42mLogin Successfully: %s\033[0m'%userName[9:len(userName)])
        else: 
            print('\033[0;37;41mLogin Failed\033[0m')
            return

    except Exception as e:
        print('\033[0;37;41mLogin Failed:%s\033[0m'%e)

    print('Write Down the contestID:',end='')

    contestID = input()
    while True:
        time.sleep(3)
        os.system('clear')
        print('\033[0;37;42mPlayer:{} Contest: {}\033[0m'.format(CF_USER['handle'],contestID))
        print('Submit Problem: ',end='')
        problemID = input() # 读入需要提交的题号
        if problemID == 'quit': return

        rb.open('https://codeforces.com/contest/%s/submit'%contestID)
        submit_form = rb.get_form(class_='submit-form')
        submit_form['submittedProblemIndex'] = problemID

        # 找到对应代码
        Source = ''
        path = os.getcwd()
        filenames = os.listdir(path)
        for filename in filenames:
            if filename.startswith(problemID): 
                Source = filename
                break

        if Source=='' :
            # 找不到对应代码
            print('\033[0;37;41mNo Such File\033[0m')
            continue

        # 提交代码
        submit_form['sourceFile'] = Source
        rb.submit_form(submit_form)

        # 提交验证
        if rb.url[-2:] != 'my':
            print('\033[0;37;41mSubmit Failed\033[0m')
            continue

        # 成功提交
        print('\033[0;37;42mWaiting For Pending: %s => \033[0m'%Source,end='')
        print('\033[0;37;42m{} {}\033[0m'.format(contestID,problemID))


if __name__ == '__main__':
    main()
