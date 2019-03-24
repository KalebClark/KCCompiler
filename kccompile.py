#!/usr/local/bin/python3.7
# KC Compiler
# Profile based task manager for compiling quake style games.
#
# Looks for a file with the name of the second argument in the
# folder. If found, it will run the list of tasks in that order.
# if no argument is given, it will run basic compiling tasks. 

# Compiling Tasks in order:
# qbsp -> light -> vis -> copy to game/maps forlder -> execute Q.
import re
import sys
import json

class KCC:
    config = {}
    command = ""
    map_profile = ""
    build_profile = ""

    def __init__(self):
        self.config = KCCConfig()
        self.parseArgs()

    def parseArgs(self):
        #print(len(sys.argv))
        # Check for arguments
        if len(sys.argv) <= 1:
            self.help()
            sys.exit(1)

        # Handle Command
        cmd = sys.argv[1]
        self.command = cmd

        # is it build?
        match = re.match("^build:.*", cmd)
        if match is not None:
            self.build_profile = self.command.split(':')[1]
            self.command = 'build'

        # is it newBuild?
        match = re.match("^newBuild:.*", cmd)
        if match is not None:
            self.build_profile = self.command.split(':')[1]
            self.command = 'newBuild'

        # is it newMap
        match = re.match("^newMap:.*", cmd)
        if match is not None:
            self.map_profile = self.command.split(':')[1]
            self.command = 'newMap'

        # Handle Map Profile
        if len(sys.argv) > 2:
            self.map_profile = sys.argv[2]

    def help(self):
        print("Usage:   kccompile <command>:<profile> <map profile>")
        print("Example: kccompile build:fast e1m2")
        print("\tCommands: ")
        print("\t\tnewBuild:<profilename>\tScaffold new build build profile")
        print("\t\tbuildProfiles\tShows all build profiles")
        print("\t\tnewMap:<mapname>\tScaffold new map profile")
        print("\t\tmapProfiles\tShows all map profiles")
        print("\t\tbuild:<profile>\tExecutes build profile")
        print("\t\tplay\t\tSkips compilation. Play last compiled map in map profile")

    def build(self):
        pass

    def play(self):
        pass

class KCCConfig:

    config = {}

    def __init__(self):
        self.load()

    def load(self):
        """ Load the config file. Create basic config file if empty
        ================================================================= """

        with open('config.json') as config_json:
            try:
                self.config = json.load(config_json)
            except json.decoder.JSONDecodeError:
                print("File does not contain any JSON. Creating new config")
                self.config = {"builds": [], "maps": []}

        config_json.close()

    def save(self):
        """ Save Config file 
        ================================================================= """
        with open('config.json', 'w') as config_output:
            json.dump(self.config, config_output, indent=2, separators=(',', ': '))
        config_output.close()

    def buildExists(self, build_name):
        """ Check to see if build exists. Return bool
        ================================================================= """
        for build in self.config['builds']:
            if build['name'] == build_name:
                return True
        return False

    def mapExists(self, map_name):
        """ Check to see if map exists. Return bool
        ================================================================== """
        for mmap in self.config['maps']:
            if mmap['name'] == map_name:
                return True
        return False

    def newBuild(self, build_name):
        """ Create new build from scaffold.
         ================================================================= """
        scaffold = {
            "name": build_name,
            "tools": [
                {"name": "qbsp", "path": False, "args": []},
                {"name": "light", "path": False, "args": []},
                {"name": "vis", "path": False, "args": []}
            ]
        }
        if self.buildExists(build_name):
            print("Build: " + build_name + " already exists. Not Creating")
            return False
        else:
            print("Creating new build: " + build_name)
            self.config['builds'].append(scaffold)

    def newMap(self, map_name):
        """ Create new map from Scaffold
        ================================================================== """
        scaffold = {
            "name": map_name,
            "game": "",
            "map_source": "",
            "map_dest": ""
        }
        if self.mapExists(map_name):
            print("Map: " + map_name + " already exists. Not Creating")
            return False
        else:
            print("Creating new map profile: " + map_name)
            self.config['maps'].append(scaffold)

    def showOpts(self, tool):
        """ Show args for specified tool
        ================================================================= """
        for opt in tool['args']:
            print(opt)

    def argsToCommand(self, args):
        """ Convert list of arguments to formatted command line
        ================================================================= """
        return " ".join(args)

    def show(self):
        """ Dump full config
        ================================================================= """
        print(self.config)

    def showBuilds(self):
        """ Show the builds to user
        ================================================================= """
        builds = self.config['builds']

        # Builds are a list
        for build in builds:
            print("BUILD: --> " + build['name'] + " <--")
            for tool in build['tools']:
                print("\tTOOL: " + tool['name'])
                
                # Show PAth
                if not tool['path']:
                    tool_path = "Using Default"
                else:
                    tool_path = tool['path']
                print("\tPATH: " + tool_path)

                # Show Args
                args = self.argsToCommand(tool['args'])
                print("\tARGS: " + args)

                print("")
    def showMaps(self):
        """ show map profiles to the user
        ================================================================= """
        maps = self.config['maps']

        for map in maps:
            print("MAP: --> " + map['name'] + " <--")
                

            #self.showOpts(builds['qbsp'])



# == End KCC Class ============================================================        

def main():
    """ Main Entry Point """

    #config = KCCConfig()
    #App = KCC(KCCConfig())
    App = KCC()
    print("App.command:\t\t" + App.command)
    print("App.build_profile:\t" + App.build_profile)
    print("App.map_profile:\t" + App.map_profile)

    if App.command == 'newBuild':
        App.config.newBuild(App.build_profile)
        App.config.save()
    elif App.command == 'buildProfiles':
        App.config.showBuilds()
    elif App.command == 'newMap':
        App.config.newMap(App.map_profile)
        App.config.save()
    elif App.command == 'mapProfiles':
        App.config.showMaps()
    elif App.command == 'play':
        App.play()
    else:
        App.help()


    #config.newBuild('wowzers')

    #config.showBuilds()
    #config.save()

    
if __name__ == '__main__':    
    sys.exit(main())
