import os
import sys
from getopt import getopt


class BuildImage:

    _REGISTRY_HOST = os.environ.get('DOCKER_REGISTRY')

    if _REGISTRY_HOST is None:
        raise EnvironmentError('DOCKER_REGISTRY Not Found')

    @classmethod
    def publish(cls):
        opts, args = getopt(sys.argv[1:], 'n:f:t:')
        opts_dict = dict(opts)
        if '-t' not in opts_dict:
            sys.exit('missing tag arguments')
        tag = opts_dict['-t']
        if '-n' and '-f' in opts_dict:
            project_name = opts_dict['-n']
            docker_file = opts_dict['-f']
        else:
            project_path = os.getcwd()
            os.chdir(project_path)
            project_name = os.path.basename(project_path)
            docker_file = None

        print()
        option = input(f'Publish Image {docker_file} => {cls._REGISTRY_HOST}/{project_name}:{tag}? (y/ n)')
        if option.lower() not in ['y', 'yes']:
            sys.exit()
        if docker_file:
            os.system(f'docker build -t {project_name} -f {docker_file} . --no-cache')
        else:
            os.system(f'docker build -t {project_name} . --no-cache')
        os.system(f'docker tag {project_name} {cls._REGISTRY_HOST}/{project_name}:{tag}')
        os.system(f'docker push {cls._REGISTRY_HOST}/{project_name}:{tag}')

if __name__ == '__main__':
    BuildImage.publish()
