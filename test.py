import subprocess

if __name__ == '__main__':
        p = subprocess.Popen("ping -c1 -W1  iphone-de-sebastien.home | grep -o -E '[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3}'", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        print(output)
        if output:
            print("Yay, the devine is connected to your network!")
        else:
            print("The device is not present!")