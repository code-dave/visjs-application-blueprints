#compiling py data into visjs formatting, linking scripts/file, class, function, and variable architecture.
# input python files you desire to be parsed.
file_list = ['testfile_1.py', 'testfile_2.py', 'somestuff.py']
def parse_pyfiles():
    vjs_raw = {}
    for file in file_list:
        print(file)
        comments = []
        vjs_raw[file] = {
        #'comments': [],
        'classes': {},
        'functions': [],
        'imports': {}, 
        }
        with open(file, 'r') as f:
            r = f.read()
            sc = '\r\n' if '\r\n' in f else '\n'
            fs = r.split(sc)
            while fs:
                #removes spaces, and unwanted padding
                line = fs[0].strip()
                # .0 ignore all mass commented code i.e == ''' code '''
                if line.startswith("'''"):
                    print(f'[I] first line of mass comment {line}')
                    n = 0
                    while fs[n].strip() != "'''":
                        print(f'[I] ignoring: {fs[n]}')
                        del fs[n]
                        n = n + 1
                    del fs[0]
                #  .1 parsing imports, using nested dicts
                elif line.startswith('from ') or line.startswith('import '):
                    #local var assgined for a class or function, previously line[0] imported
                    line2 = fs[1].strip()
                    if ' import *' in line:
                        library = line.split(' ')[1]
                        if library not in vjs_raw[file]['imports']:
                            vjs_raw[file]['imports'][library] = []
                        else:
                            pass
                    elif 'import' in line and 'from' not in line and 'as ' not in line:
                        library = line.split(' ')[1]
                        if library in vjs_raw[file]['imports']:
                            vjs_raw[file]['imports'][library].append(library)
                        else:
                            vjs_raw[file]['imports'][library] = []
                    elif ' as ' in line:
                        library_global = line.split(' ')[1]
                        library_local = line.split(' ')[-1]
                        if library_global in vjs_raw[file]['imports']:
                            vjs_raw[file]['imports'][library_global].append(library_local)
                        else:
                            vjs_raw[file]['imports'][library_global] = []
                            vjs_raw[file]['imports'][library_global].append(library_local)
                    elif 'from' in line or 'import' in line:
                        library = line.split(' ')[1]
                        sub_lib = line.split(' ')[-1]
                        if library in vjs_raw[file]['imports']:
                            vjs_raw[file]['imports'][library].append(sub_lib)
                        else:
                            vjs_raw[file]['imports'][library] = []
                            vjs_raw[file]['imports'][library].append(sub_lib)
                    if ' = ' in line2:
                        for library in vjs_raw[file]['imports'].keys():
                            if str(library) in str(line2.split(' ')[-1]) or str(library) in str(line2.split(' ')[-1].split('()')[0]):
                                local_sym = line.split(' ')[0]
                                vjs_raw[file]['imports'][library].append(local_sym)
                            else:
                                pass
                        del fs[1]
                    del fs[0]
                # .2 parse commented lines, and any multi line comments
                # lines are appended to global comments = [] and then later pulled into:
                # Classes, Functions and some variables when applicable.
                #elif line.startswith('#') and "'''" not in line and 'print' not in line:
                #    del fs[0]
                #    com = line.split('#')[-1].strip()
                #    comments.append(com)
                #    print(f'[I] comment {line}')
                #    n = 2
                #    while fs[n].startswith('#'):
                #        n = n + 1
                #        print(f'[I] comment more {line}')
                #        com = line.split('#')[-1].strip()
                #        comments.append(com)
                #        del fs[n]
                #    del fs[0]
                # .3 parse class data, and generate function, var, comment keys for all nested data.
                elif line.startswith('class'):
                    clazz = line.split(' ')[1].split('(')[0]
                    vjs_raw[file]['classes'][clazz] = {
                    'functions': [],
                    'variables': [],
                    'comments': [],
                    }
                    del fs[0]
                #elif line.startswith(''):
                # .4 parse function data, and add comments if applicable
                elif line.startswith('def'):
                    function = line.split('def ')[1].split(':')[0]
                    if len(vjs_raw[file]['classes'].keys()) > 0:
                        for clazz in vjs_raw[file]['classes']:
                            vjs_raw[file]['classes'][clazz]['functions'].append(function)
                    else:
                        if len(comments) > 0:
                            func = {
                            function: comments,
                            }
                            vjs_raw[file]['functions'].append(func)
                            comments = []
                        else:
                            vjs_raw[file]['functions'].append(function)
                    del fs[0]
                else:
                    pass
                del fs[0]
    return vjs_raw
def visjs_format():
    vjs_raw = parse_pyfiles()
    # {id: 1, label:'html color', color: 'lime'},
    nodes = []
    # {from: 1, to: 3},
    edges = []
    #scripts
    #print(vjs_raw)
    n = 1
    for file in vjs_raw:
        print('FILE value:', file)
        entry = {
        'id': n,
        'label': file,
        'color': '#005EB8',
        'border': '#00BF6F',
        }
        parent = n
        path = {
        'from': '', 'to': '',
        }
        nodes.append(entry)
        n = n + 1
        #comments, classes, functions, and imports
        # obj types will be used for referencing objs, no entry needed
        for x in vjs_raw[file]:
            print('X value:', x)
            #class: functions, vars, comments
            #global functions: function name and comments
            #classes: comments
            for y in vjs_raw[file][x]:
                #
                print('Y value:', y)
                # going into the nested class
                if x == 'classes':
                    for z in vjs_raw[file][x][y]:
                        print('Z value:', z)
                        if z == 'functions':
                            for zz in vjs_raw[file][x][y][z]:
                                print('ZZ value:', zz)
                                entry = {
                                    'id': n,
                                    'label': zz,
                                    'color': '#DBE2E9',
                                    'border': '#FE5000',
                                }
                                path = {
                                    'from': parent, 'to': n
                                }
                                n = n + 1
                                nodes.append(entry)
                                edges.append(path)
                        elif z == 'imports':
                            entry = {
                                'id': n,
                                'label': z,
                                'color': '#FE5000',
                                'border': '#FFC72C',
                            }
                            path = {
                                'from': parent, 'to': n
                            }
                            n = n + 1
                            #print('file --',file, 'parent --', x,'child--',y,'grandchild --',z)
                            nodes.append(entry)
                            edges.append(path)
                        # functions within a class
                        else:
                            pass
                #non-class scripts
                #
                # imports
                elif x == 'imports':
                    #print('file --',file, 'parent --', x,'child--',y)
                    entry = {
                        'id': n,
                        'label': y,
                        'color': '#FE5000',
                        'border': '#FE5000',
                    }
                    path = {
                        'from': parent, 'to': n
                    }
                    n = n + 1
                    nodes.append(entry)
                    edges.append(path)
                # exception for class data
                elif x == 'functions' or x == 'comments':
                    pass
                #non-class scripts, usually global functions
                else:
                    #print('file --',file, 'parent --', x,'child--',y)
                    entry = {
                        'id': n,
                        'label': y,
                        'color': '#DBE2E9',
                        'border': 'FE5000',
                    }
                    path = {
                        'from': parent, 'to': n
                    }
                    n = n + 1
                    nodes.append(entry)
                    edges.append(path)
    for r in edges:
        print(f'  {r},')
    for r in nodes:
        print(f'  {r},')
    return(nodes, edges)
        

'''
vjs_raw
1. files
	a. comments
	b. classes
		* key: class name
			- functions
				^ key: function name | value: comments
			- variables
			- comments
	c. functions
		* key: function name | value: comments
	d. imports
		* key: import
			- key: libary name | value: (more specific) imports or local assigned vars
javascript structure: list with each item have dict = {'id': '', label: '', color:'',}
example:
[
    {id: 1, label:'html color', color: 'lime'},
    {id: 2, label:'rgb color', color: 'rgb(255,168,7)'},
    {id: 3, label:'hex color', color: '#7BE141'},
    {id: 4, label:'rgba color', color: 'rgba(97,195,238,0.5)'},
    {id: 5, label:'colorObject', color: {background:'pink', border:'purple'}},
    {id: 6, label:'colorObject + highlight', color: {background:'#F03967', border:'#713E7F',highlight:{background:'red',border:'black'}}},
    {id: 7, label:'colorObject + highlight + hover', color: {background:'cyan', border:'blue',highlight:{background:'red',border:'blue'},hover:{background:'white',border:'red'}}}
  ]
  
'''
