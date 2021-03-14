import sys
import os


class ExecContainer:
    @classmethod
    def exec_container(cls):
        args = sys.argv
        if len(args) < 2:
            sys.exit()
        name_filter = args[1]
        command = f'kubectl get pods -o=name --all-namespaces | grep {name_filter}'
        pod_list = os.popen(command).readlines()
        pod_list = [pod.strip() for pod in pod_list]
        if not pod_list:
            sys.exit('POD NOT FOUND')
        else:
            if len(pod_list) == 1:
                pod = pod_list[0]
            else:
                print('PLEASE ENTER POD NUMBER:')
                menu_str = '\n'.join([f'【{index}】: {pod}' for index, pod in enumerate(pod_list)])
                pod_index = input(f'{menu_str}\n')
                pod = pod_list[int(pod_index)]
            print(f'POD {pod} FOUND')
            command = f'kubectl exec -it {pod} -- bash'
            os.system(command)

if __name__ == '__main__':
    ExecContainer.exec_container()
