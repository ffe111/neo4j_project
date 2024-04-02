#! /usr/bin/env python3
"""
This program is 'menu.py'
menu for main_menu 
use to get input and call func
"""
class BackMenu(Exception):
    pass

def case1(*, driver):
    print('Case1')
    return 

def case2(*, driver):
    print('Case1')
    return 

def get_choice(*,msg="Please enter choice: ", choice_data):
    # choice_data.append("[Back to Main Menu]")
    max_len = len(choice_data)
    while True:
        for numb, data in enumerate(choice_data, start=1):
            print(f"{numb}: {data}")
        try:
            print("─"*70)
            print(f"0: [Back to Main Menu]")
            print("─"*70)
            choice = int(input(f"{msg}"))
            if choice == 0:
                raise BackMenu("Go to Main Menu")
            if choice <= max_len and choice > 0:
                print(f"You choose {choice} is '{choice_data[choice-1]}'")
                return choice_data[choice-1]
            else:
                raise ValueError("Invalid input")
        except (ValueError, EOFError) as xcpn:
            print(f"Please enter value choice. (between 1-{max_len})")

def main_menu(*, mdata, driver):
    while True:
        print("═"*70)
        print(f"{'Main Menu':^70s}")
        print("*"*70)
        for index, entry in enumerate(mdata,start=1):
            print(f"{index:d}.  {entry[0]:s}")
        print(f"{index+1:d}.  Exit\n")
        try:
            print("═"*70)
            inval = input(f"Enter choice: ")
        except EOFError:
            print()
            inval = None
        try:
            choice = int(inval)
        except (TypeError,ValueError) as xcpn:
            choice = 0        # 0 is never valid
        if not (1 <= choice <= (index+1)):
            print(f"Invalid choice '{inval}'!")
            continue
        if choice == index+1: # synthetic exit choice
            return EXIT_SUCCESS
        mdata[choice-1][1](driver=driver)  # call function associated with choice

def main():
    try:
        return main_menu(mdata=[("Dump Categories", case1),
                                ("Dump Locations", case2)],
                         driver=None)
    except KeyboardInterrupt:
        # they hit ctl-c
        print("\nProgram Exit by user request ctl-c!")
        return EXIT_FAILURE
    
EXIT_SUCCESS=0 
EXIT_FAILURE=1
    
if __name__ == "__main__":
    raise SystemExit(main())
