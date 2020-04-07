def append_parent_path(generation=1):
    import os, sys
    path_folder = os.path.abspath(__file__).split('/')
    go_up = -(1 + generation)
    path = '/'.join(path_folder[:go_up])
    sys.path.append(path)
    print(f'[INFO      ] | Append path: "{sys.path[-1]}"')

if __name__ == '__main__':
    append_parent_path()

