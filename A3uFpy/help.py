# main_help = "Why are buttons disabled?\nYou need to set the database first in settings."
main_help = """
<h3>What is this?</h3>
This is a program developed at CalStateLA for the automatic analysis of archeological micro-fauna.
This is still in development.
<h3>Why is the database button disabled?</h3>
You need to set the database first in settings.
<h3>Why is the measure button disabled?</h3>
You need to go in settings and make sure all the instuments are connected (the connect button becomes green for each instrument)
"""

instrumentation_help="""
<h3>What is this?</h3>
Tab to search, connect, and configure relevant instrumentation.
<h3>OS is blocking access to the port</h3>
Your operative system (ususally linux or macos) is blocking access to the ports.
Go on the git https://github.com/GiorgiArch/A3uF and under tools, download the unlock ports script.
Run the script at your own risk.
To run the script, open a terminal in the local directory where you downloaded the script and type "sudo sh unblock_ports.sh".
Reboot the pc and it should work.
"""
