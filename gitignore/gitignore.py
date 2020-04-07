# To create a default .gitignore
import os

def isRoot():
    # ls當前資料夾
    ls = os.listdir(".")
    if ".git" in ls:
        return True
    else:
        return False

def isY_N():
    while True:
        info = "\n .gitignore exist!\n - 'Y' to overwrite it. \n - 'N' to extract.\n"
        print(info)
        opt = input(">>> ")
        if opt.upper() in ("Y","YES"):
            return True
        elif opt.upper() in ("N","NO"):
            return False
        else:
            err_invalid = "\nInvalid Input!\n"
            print(err_invalid)


def isExist():
    # ls當前資料夾
    ls = os.listdir(".")
    if ".gitignore" in ls:
        if isY_N() == True:
            # 同意覆寫，回傳False 視檔案不存在
            return False
        return True
    else:
        # 檔案不存在
        return False

def main():
    if isRoot() == True:
        if isExist() == True:
            quit("Program has been terminated!")
        else:
            with open('.gitignore', 'wt') as f:
                f.write(".DS_Store\n__pycache__\n")
            info_finish = "Done!"
            print(info_finish)
    else:
        err_wrongDir = "Could not find '.git'"
        print(err_wrongDir)

if __name__ == "__main__":
    main()
