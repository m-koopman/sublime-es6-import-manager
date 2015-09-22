
import sublime, sublime_plugin
import subprocess
from subprocess import Popen, PIPE, STDOUT

def extract_quotes(text):
    import re
    matches=re.findall(r'[\"\'](.+?)[\"\']',text)
    return ",".join(matches)

class Es6ImportManagerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        empty = True
        sel = self.view.sel()
        for region in sel:
            if ( region.size() > 0 ):
                empty = False
                break

        if empty:
            region = sublime.Region(0, self.view.size())
        else:
            region = sel[ 0 ]

        if not region.empty():
            s = self.view.substr(region)

            output = self.reorder( s )

            self.view.replace(edit, region, output)


    def reorder( self, string ):
        requires = []
        raw_imports = []
        imports = []
        remainder_index = -1
        lines = string.split("\n")
        for line in lines:
            remainder_index += 1
            line = line.strip()
            if ( line == "" ):
                continue
            if "import" in line:
                path = extract_quotes( line )
                if "/" in path:
                    imports.append( line )
                else:
                    raw_imports.append( line )
                continue
            if "require" in line:
                requires.append( line )
                continue

            break

        # Don't reorder requires for now
        sorted_requires = requires #sorted( requires, key=lambda s: extract_quotes( s ) )
        sorted_raw_imports = sorted( raw_imports, key=lambda s: extract_quotes( s ) )
        sorted_imports = sorted( imports, key=lambda s: extract_quotes( s ) )

        res = []
        for line in sorted_requires:
            res.append( line )

        if ( len( sorted_requires ) > 0 ):
            res.append( "" )

        for line in sorted_raw_imports:
            res.append( line )

        last_prefix = ""
        for line in sorted_imports:
            path = extract_quotes( line )
            prefix = path[ : path.rfind( "/" ) ]

            if not ( prefix == last_prefix ):
                res.append( "" )

            last_prefix = prefix
            res.append( line )

        res.append( "" )

        res.extend( lines[ remainder_index: ] )

        return "\n".join( res )


