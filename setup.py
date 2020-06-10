import subprocess
import crontab
import json
import os
import re


def main():
    new = filter_input("Would you like to configure a new Google DDNS Updater?: ")
    delete = filter_input("Would you like to delete an existing Google DDNS Updater?: ")
    if new == 'yes' and delete == 'yes':
        delete_updater()
        create_updater()
    elif new == 'yes' and delete == 'no':
        create_updater()
    elif new == 'no' and delete == 'yes':
        delete_updater()
    else:
        exit()


# Filter input to return yes or no
def filter_input(prompt):
    input_str = input(prompt)
    filtered_str = ("no" if ((input_str.lower() == "no")
                    or (input_str.lower() == "n"))
                    else "yes")
    return filtered_str


def create_updater():
    print('\nDDNS Updater New Config')

    # Found In The Dynamic DNS Drop Down
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    hostname = input("Enter Hostname: ")

    offline = filter_input("Would you like to set status to offline? (y/n): ")

    with open('config.json', 'w') as config:
        json.dump({"username": username,
                   "password": password,
                   "hostname": hostname,
                   "offline": offline}, config, indent=4)

    subprocess.run(['python', f'{os.getcwd()}/update.py'])

    # Create cronjob to automatically update DDNS
    with crontab.CronTab(user=True) as cron:
        job = cron.new(command=f'python {os.getcwd()}/update.py', comment=f'DDNS Updater: {hostname}')
        job.hour.every(1)
        print(job.every().hour())


def delete_updater():
    print('\nDDNS Updater Delete Config')

    hostname = input("Enter hostname for Google DDNS Updater to be deleted: ")

    # Deletes cronjob matching given hostname
    with crontab.CronTab(user=True) as cron:
        cron.remove_all(comment=re.compile(fr'\b{hostname}'))

    print(f'{hostname} Config Deleted!')


if __name__ == '__main__':
    main()
