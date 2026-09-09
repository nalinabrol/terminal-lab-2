from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'Lab_2_Terminal_Tools_Student_Booklet.pdf'
TEXT = ROOT/'Lab_2_Terminal_Tools_Student_Booklet.md'
FONT = Path('/System/Library/Fonts/Supplemental')
font_files=[('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf'),('Mono','Courier New.ttf')]
if not (FONT/'Arial.ttf').exists():
    FONT=Path('/usr/share/fonts/truetype/dejavu')
    font_files=[('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf'),('Mono','DejaVuSansMono.ttf')]
for name,file in font_files:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
GREEN_DARK=colors.HexColor('#0E6A50'); MINT=colors.HexColor('#18CB96'); INK=colors.HexColor('#373643'); GRAY=colors.HexColor('#55526A'); PALE=colors.HexColor('#EAFAF4'); LINE=colors.HexColor('#B7D9CC')
styles={
 'body': ParagraphStyle('body',fontName='Body',fontSize=10.3,leading=14.1,textColor=INK,spaceAfter=6),
 'small': ParagraphStyle('small',fontName='Body',fontSize=9.1,leading=12.2,textColor=GRAY,spaceAfter=5),
 'h': ParagraphStyle('h',fontName='Bold',fontSize=12,leading=15,textColor=GREEN_DARK,spaceBefore=12,spaceAfter=6),
 'title': ParagraphStyle('title',fontName='Bold',fontSize=23,leading=27,textColor=GREEN_DARK,spaceAfter=9),
 'kicker': ParagraphStyle('kicker',fontName='Bold',fontSize=9,leading=12,textColor=GREEN_DARK,spaceAfter=8),
 'code': ParagraphStyle('code',fontName='Mono',fontSize=9.1,leading=12.3,textColor=INK,spaceAfter=0),
 'table': ParagraphStyle('table',fontName='Body',fontSize=9,leading=11.9,textColor=INK),
}
W=511.27
story=[]; md=[]
class Lines(Flowable):
 def __init__(self,n=1): Flowable.__init__(self); self.width=W;self.height=n*20;self.n=n
 def draw(self):
  self.canv.setStrokeColor(LINE);self.canv.setLineWidth(.5)
  self.canv.setDash(2, 3)
  for i in range(self.n):self.canv.line(12,self.height-16-i*20,W-12,self.height-16-i*20)
  self.canv.setDash()

def para(s,kind='body'):
 story.append(Paragraph(s,styles[kind]));md.append(s.replace('<b>','**').replace('</b>','**').replace('<br/>','\n'))
def h(s):para(s,'h')
def code(s):
 p=Paragraph(escape(s).replace(' ','&#160;').replace('\n','<br/>'),styles['code'])
 box=Table([[p]],colWidths=[W]);box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 story.extend([box,Spacer(1,7)]);md.append('```bash\n'+s+'\n```')
def lines(label,n=1):
 para(label,'small')
 if n:
  story.append(Lines(n));md.append('_' * 65 + '\n')
 story.append(Spacer(1,10 if n == 0 else 3))
def table(rows,widths,compact=False):
 cells=[[Paragraph(escape(c).replace('\n','<br/>'),styles['table']) for c in row] for row in rows]
 t=Table(cells,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.6,LINE),('LINEBELOW',(0,1),(-1,-1),.3,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3 if compact else 6),('BOTTOMPADDING',(0,0),(-1,-1),3 if compact else 6)]));story.extend([t,Spacer(1,7)]);md.extend([' | '.join(row) for row in rows])
def page(kicker,title):
 if story:story.append(PageBreak());md.append('\n---\n')
 para(kicker,'kicker');para(title,'title')
def step(label,text):para('<b>'+label+'</b> '+text)
def start():para('<b>Start:</b> your lab root - the absolute path you wrote on page 1. Begin each experiment here unless instructed otherwise.','small')

page('LAB 2 / TERMINAL TOOLS', 'Clean up the event records')
para('Student experiment booklet | Bash in GitHub Codespaces | About 100 minutes')
lines('Name: __________________________  Lab ID: ______________  Section: __________', 0)
para('Your event team has draft notices, repeated registrations and conflicting timetables. Learn seven tools, investigate the records, and prepare a reliable set of files.')
h('Get ready')
para('Sign in with your GitHub account. Your instructor must grant access while this repository is private. Open the Lab 2 link below and create a Codespace on <b>main</b>, or resume your Lab 2 Codespace. Lab 1 uses a different repository.')
para('<link href="https://codespaces.new/nalinabrol/terminal-lab-2?quickstart=1" color="#0E6A50"><u>Open the Lab 2 Codespace</u></link> | github.com/nalinabrol/terminal-lab-2', 'small')
para('Wait for setup. Choose <b>Trust Folder &amp; Continue</b> if asked. A maximized Bash terminal opens after startup. At the repository root, run:')
code('bash terminal-lab-2/start.sh')
para('Enter your instructor-assigned ID. Run the exact <b>cd</b> command printed by setup, then run <b>pwd</b> and <b>cat identity.txt</b>. Reusing an ID preserves the existing attempt; it does not reset mistakes.')
lines('My lab root (the full path printed by pwd):', 2)
lines('EVENT: __________________  ROOM: _________________  TIME: ______________', 0)
table([['Folder', 'Purpose'], ['practice/', 'Original evidence for guided experiments. Keep it unchanged.'], ['challenge/', 'Fresh evidence for your independent mission. Keep it unchanged.'], ['work/', 'Your working copies and saved results. Already created for you.']], [100,W-100])
para('<b>How to work:</b> predict, try, inspect, and explain. Begin every experiment at your lab root. Type one command at a time. Use the terminal and nano for edits; do not generate solution scripts. Write observations, not entire screen transcripts.', 'small')
para('Hints: page 12. Command reference: page 13. Save your work in this Codespace. The checker does not submit files. No permissions, environment-variable, or scripting lesson is required.', 'small')

page('EXPERIMENT 1 / 8 MINUTES', 'Find a command you used before')
start()
h('1A | Make a small trail')
para('Type and run these commands <b>one at a time</b>. They provide a known trail to search in your own terminal history.')
code('grep -F "EVENT=" identity.txt\ngrep -F "ROOM=" identity.txt\nhistory 10')
para('<b>history</b> lists remembered commands with numbers. <b>history 10</b> shows up to ten recent entries. Your numbers may differ from a classmate\'s. Lab 1 used Up Arrow; today you will search instead of stepping through every command.')
lines('Which number is beside your ROOM search? __________', 0)
h('1B | Filter the history list')
code('history | grep -F "identity.txt"')
para('This reuses Lab 1\'s pipe and text search to search <b>command text</b>. The history-search command itself may also appear because it contains identity.txt.')
lines('Write one earlier matching command, excluding the history search itself:')
h('1C | Search interactively, then edit')
para('At an empty Bash prompt, press <b>Ctrl+R</b>. Type <b>grep -F</b> slowly. The matching command appears. Press Ctrl+R again to find an older match. Stop at the command that searches ROOM or EVENT.')
para('Press <b>Right Arrow</b> to accept that command for editing without running it. Use the arrow keys and Backspace to change the quoted search text to <b>TIME=</b>. Inspect the whole line, then press Enter.')
lines('What did your edited command print?')
h('1D | Leave a search without running it')
para('From an empty prompt, press Ctrl+R, type <b>identity</b>, then press <b>Ctrl+G</b>. This cancels the search and restores the input you had before it. No matched command should run.')
para('Click inside the terminal before using shortcuts. Use <b>Control</b>, not Command, on a Mac. If the browser intercepts a shortcut, use the history-list method and ask your instructor for help.', 'small')
lines('Show your instructor: find an older command, edit it, and explain before running it.', 0)

page('EXPERIMENT 2 / 10 MINUTES', 'Repair a notice with nano')
start()
para('<b>nano</b> is a text editor inside the terminal. Unlike echo with redirection, it lets you move to and edit an existing line.')
h('2A | Inspect before changing')
code('cat identity.txt\ncat work/notice.txt\nnano work/notice.txt')
para('Use the arrow keys to move. Change <b>Room: Hall-0</b> to your ROOM from identity.txt. Keep the text <b>Room: </b> before the value. Do not change the event code.')
table([['Keys', 'In nano'], ['Arrow keys / Backspace', 'Move the cursor / remove the character before it.'], ['Ctrl+O, then Enter', 'Write the file; confirm its existing filename.'], ['Ctrl+X', 'Exit nano. If asked to save changes, choose Y and confirm the filename.']], [160,W-160])
para('Nano displays Control shortcuts with a caret: <b>^O</b> means Ctrl+O. It does not mean type the two characters ^ and O.')
h('2B | Save, exit, and verify')
para('Save your room change and exit. Run <b>cat work/notice.txt</b>. Then reopen it in nano to confirm that the saved change is still there.')
lines('What evidence shows that your edit was saved?')
h('2C | Finish independently')
para('Update <b>Doors open:</b> to your TIME from identity.txt. Add a fourth line containing exactly <b>Bring your student card.</b> Save and exit. Your file must contain exactly four lines in the order shown below, using your own values:')
code('Event: YOUR_EVENT\nRoom: YOUR_ROOM\nDoors open: YOUR_TIME\nBring your student card.')
para('YOUR_EVENT, YOUR_ROOM and YOUR_TIME above are placeholders, not text to leave in the file. Finish the final line with Enter so it ends with a newline.', 'small')
lines('My final room: ______________  My final opening time: ______________', 0)

page('EXPERIMENT 3 / 8 MINUTES', 'Find the current instruction')
start()
para('A long file is hard to inspect with cat. <b>less</b> lets you scroll and search without changing the file.')
code('less practice/handbook.txt')
table([['Keys', 'In less'], ['Space / b', 'Move forward / backward by one screen.'], ['g / G', 'Jump to the beginning / end. Use Shift+g for uppercase G.'], ['/COLLECTION, then Enter', 'Search forward for COLLECTION.'], ['n / N', 'Next / previous match of that search.'], ['q', 'Quit less and return to Bash.']], [185,W-185])
h('3A | Predict, then compare')
para('Start at the beginning with <b>g</b>. Search for COLLECTION. Read the heading and the next lines. Is the first matching instruction necessarily the correct one?')
lines('First heading found:')
para('Use <b>n</b> to find later matches. Use <b>N</b> to go back once. Find the heading <b>COLLECTION - ACTIVE</b> with your EVENT code.')
lines('Why should the archived and other-event instructions be rejected?')
h('3B | Save the answer')
para('Write down the complete sentence immediately below the ACTIVE heading. Quit less with q. Open <b>nano work/collection.txt</b> and save only that sentence on one line. Keep its capitalization and final full stop; finish with Enter.')
lines('The approved collection sentence:', 2)
h('3C | Explain the choice of tool')
lines('How does less help with this task compared with displaying the whole file using cat?', 2)
para('If you see a colon or (END), you may still be inside less. Press q before entering a shell command.', 'small')

page('EXPERIMENT 4 / 10 MINUTES', 'Put records in order')
start()
h('4A | Sort names')
code('cat practice/names.txt')
lines('Before sort: predict the first and last names. First: __________ Last: __________', 0)
code('sort practice/names.txt')
para('<b>sort</b> writes ordered lines to the terminal. It does not rewrite its input file. These files use simple names with consistent capitalization.')
para('Save the alphabetically sorted names to <b>work/names-sorted.txt</b>, then inspect the saved file. Use Lab 1\'s output redirection.')
lines('My command:')
h('4B | Are numbers just text?')
code('cat practice/scores.txt')
para('Predict both orders before running the two sort commands below. Ordinary sort compares text; <b>-n</b> compares numeric values. For this file, each line contains just one non-negative whole number.')
lines('Ordinary sort order:')
lines('Numeric sort order:')
code('sort practice/scores.txt\nsort -n practice/scores.txt')
h('4C | Highest first')
para('<b>-r</b> reverses the order. Combine it with -n to sort these scores from highest to lowest. Save the result as <b>work/scores-desc.txt</b>.')
lines('My command:')
lines('Largest score: __________  Smallest score: __________', 0)
para('Inspect practice/scores.txt again. Its original order should remain unchanged. Never use the same file as both the input and the destination of &gt;.', 'small')

page('EXPERIMENT 5 / 10 MINUTES', 'When does a duplicate disappear?')
start()
code('cat practice/repeated-names.txt')
para('Some repeated names are next to each other; others are separated. <b>uniq</b> compares adjacent lines.')
h('5A | Predict the result')
lines('Which name will still appear more than once after plain uniq?')
code('uniq practice/repeated-names.txt')
lines('Observed repeated name(s):')
h('5B | Bring matching lines together')
code('sort practice/repeated-names.txt | uniq')
para('Sorting brings identical names together. Now uniq can keep one line from each group. Save this output to <b>work/unique-names.txt</b>.')
lines('Why did sorting first change the result?', 2)
h('5C | Count each group')
code('sort practice/repeated-names.txt | uniq -c')
para('<b>-c</b> adds the number of lines in each adjacent group. Leading spaces before a count are normal. Save the counts to <b>work/name-counts.txt</b>.')
lines('One name and its count: ____________________  Count: __________', 0)
para('Add the counts mentally and compare the sum with the number of lines in the original file. This counts entries, not necessarily different people: the names in this small dataset identify fictional participants.')
lines('Sum of counts: __________  Original line count: __________', 0)
para('<b>Independent check:</b> explain why using uniq before sort is not enough to guarantee one line per name.', 'small')

page('EXPERIMENT 6 / 10 MINUTES', 'Choose the fields you need')
start()
para('Each record in this file has three fields: <b>student ID | name | workshop</b>. There is no header row. The vertical bar separates fields; it is the delimiter.')
code('head -n 3 practice/registrations.txt\ncut -d "|" -f 2 practice/registrations.txt')
para('<b>cut -d "|"</b> selects the field separator; <b>-f 2</b> selects field 2. Quote the separator so Bash passes it to cut instead of treating it as a pipeline.')
lines('From the first record: field 1 = __________  field 2 = __________  field 3 = __________', 0)
h('6A | Save the names')
para('Extract every name to <b>work/registration-names.txt</b>. Preserve the original row order and repetitions. Do not sort this output.')
lines('My command:')
h('6B | Select more than one field')
code('cut -d "|" -f 1,3 practice/registrations.txt')
para('Save that result to <b>work/id-workshop.txt</b>. Notice that cut keeps the delimiter between the selected fields.')
lines('What is missing from this result compared with the original file?')
h('6C | Count workshop registrations')
para('Extract workshop choices into <b>work/workshops.txt</b>. Then sort that file and use uniq -c. Save the counts to <b>work/workshop-counts.txt</b>. work/workshops.txt is an intermediate file, not a separate graded result.')
lines('My extraction command:')
lines('My sorting-and-counting command:')
lines('How does cut differ from grep?', 2)
para('These are simple delimiter-separated records. We are not handling quoted CSV fields, missing fields, or delimiters inside names in this exercise.', 'small')

page('EXPERIMENT 7 / 10 MINUTES', 'What changed between versions?')
start()
h('7A | Compare an identical pair')
code('diff practice/timetable-before.txt work/timetable.txt')
para('<b>diff FIRST SECOND</b> reports line differences. No output means no differences were found. A missing file produces an error instead.')
lines('What did you observe?')
h('7B | Compare the old and approved versions')
code('diff practice/timetable-before.txt practice/timetable-approved.txt')
table([['Marker', 'Meaning in this output'], ['<', 'This line is from the FIRST file (old timetable).'], ['>', 'This line is from the SECOND file (approved timetable).'], ['a / c / d', 'In the numbered instruction: add / change / delete.'], ['---', 'Separates the old and new lines in a change block.']], [115,W-115])
para('For example, <b>2c2</b> means line 2 in the first file changes to line 2 in the second. <b>3d2</b> means remove line 3 from the first file; the second-file position is after line 2. Focus on the event lines under the markers.')
lines('Which event moved to a different time?')
lines('Which event was removed? Which was added?')
h('7C | Repair the working copy')
para('Open <b>nano work/timetable.txt</b>. Make the three required changes so it matches the approved timetable. Save and exit, then compare:')
code('diff work/timetable.txt practice/timetable-approved.txt')
lines('What result tells you the repair is complete?')
para('You can save a comparison with &gt;, just as in Lab 1. Do not add its output to either input file. A comparison with differences is expected here; it is not a broken command.', 'small')

page('INDEPENDENT CHALLENGE / 17 MINUTES', 'Prepare the event for opening')
para('Use only the fresh evidence in <b>challenge/</b> and working copies in <b>work/challenge/</b>. These files were created at setup, so this mission does not depend on finishing the guided experiments. Begin at your lab root.')
h('Your mission')
step('1. Discover.', 'Open <b>challenge/brief.txt</b> in less. Find <b>APPROVAL - CURRENT</b> for your EVENT. Ignore the old approval. It specifies four exact announcement lines.')
step('2. Repair.', 'Use nano to correct <b>work/challenge/announcement.txt</b> to those four lines. Preserve capitalization, punctuation and line order.')
step('3. Extract and organise.', 'Records in <b>challenge/registrations.txt</b> use the same three-field format as Experiment 6 and have no header. Produce an alphabetically sorted list of distinct names as <b>work/challenge/participants.txt</b>.')
step('4. Count.', 'Count the number of registration rows for each workshop. Save a uniq -c style report as <b>work/challenge/workshop-counts.txt</b>. Count all registrations, including repeated names.')
step('5. Compare.', 'Use diff with <b>challenge/schedule-before.txt</b> FIRST and <b>challenge/schedule-approved.txt</b> SECOND. Save its normal comparison output as <b>work/challenge/schedule-diff.txt</b>.')
step('6. Repair and verify.', 'Use nano to update <b>work/challenge/timetable.txt</b> to match the approved schedule. Compare them again to check your edits.')
h('Required results')
code('work/challenge/\n  announcement.txt\n  participants.txt\n  workshop-counts.txt\n  schedule-diff.txt\n  timetable.txt')
para('Use intermediate files in work/challenge/ if they help. Several clear commands are as valid as one long pipeline. Preserve every original file in practice/ and challenge/.', 'small')
lines('Before beginning: which tools will you combine for the participant list?', 2)

page('INDEPENDENT CHALLENGE / EVIDENCE', 'Show why your results are right')
h('Inspect your five files')
table([['Result', 'My evidence'], ['Announcement', 'Correct event, room, opening time and final instruction.'], ['Participants', 'Alphabetical order; no name occurs twice.'], ['Workshop counts', 'Counts include every registration row.'], ['Saved comparison', 'Old schedule was the first input; approved schedule was second.'], ['Repaired timetable', 'Comparison with the approved file prints no differences.']], [145,W-145])
lines('My approved event and room:', 1)
lines('Number of distinct names: ________  Total registrations: ________', 0)
h('Explain your decisions')
lines('1. Why did sorting come before removing repeated names?', 2)
lines('2. Which field did you select for workshop counts? What does each count represent?', 2)
lines('3. Which session changed time, which was removed, and which was added?', 2)
h('Use history again')
para('Find a command you used during this challenge using history search. Bring it back for inspection without running it. Show your instructor what it reads and where it writes. Cancel or clear it afterwards.')
lines('The command I chose and why:', 2)

page('EXIT CHECK / 10 MINUTES', 'Check, correct, and explain')
para('From your lab root, run the checker below. A CHECK line tells you to inspect that result. It does not repair your work.')
code('python3 ../../terminal-lab-2/check.py')
para('The checker reads 15 result files and checks that the original evidence is unchanged: <b>16 checks in total</b>. It does not upload, submit, or change files. The checker is visible; a passing score alone does not prove how you worked.')
lines('My score: ______ / 16  |  One issue I found and corrected:', 2)
h('Short understanding check')
lines('1. Why can plain sort place 100 before 2? Which option fixes numerical order?', 2)
lines('2. A name appears on lines 1 and 5. Will plain uniq necessarily remove one? Why?', 2)
lines('3. diff prints nothing. What does that establish about the two files?', 2)
h('Show a skill')
para('Your instructor may ask you to do one of these on a fresh file or with a different search: find and edit an earlier command; save a correction in nano; or locate a later matching section in less.')
lines('Skill demonstrated: ______________________  Instructor check: ______________', 0)
h('Before leaving')
para('[ ] I inspected my saved files. &nbsp; [ ] I completed the written explanations.<br/>[ ] I preserved the original evidence. &nbsp; [ ] I handed in the booklet as instructed.<br/>[ ] I kept my Codespace and lab-work folder for review.')
para('Do not delete or reset your Codespace. Follow your instructor\'s submission instructions. The checker does not submit on your behalf.', 'small')

page('OPTIONAL HINTS', 'Use one hint, then try again')
h('History')
para('Start with <b>history 10</b>. To narrow the list, pipe history into grep. For Ctrl+R, click the terminal first, use Control (not Command), and type a fragment of a command you actually ran. Right Arrow accepts a match for editing; Enter runs it; Ctrl+G cancels the search.')
h('nano')
para('The file path appears at the top of nano. Use arrows to reach the wrong text. Ctrl+O means write/save, followed by Enter to confirm the filename. Ctrl+X exits. Reopen the file or use cat to verify the result.')
h('less')
para('Press g before searching to begin at the start. Type / followed by the search word and Enter. Use n for a later match. Read the surrounding heading: archived, active and other-event entries are different. Press q before typing a shell command.')
h('sort')
para('Plain sort orders text. Add -n for numerical order and -r to reverse it. To save the output, put &gt; and the destination after the command. Input and destination must be different files.')
h('uniq')
para('If repetitions remain, inspect whether identical lines were next to one another. Put sort before uniq. Add -c to uniq for counts. Padding spaces before numbers are normal.')
h('cut')
para('Count fields from 1. The name is field 2 and workshop is field 3. -d chooses the delimiter and -f chooses fields. Quote "|" so Bash does not interpret that character as a pipe. Selecting fields preserves row order.')
h('diff')
para('Lines with &lt; come from the first file; lines with &gt; come from the second. Repair a working copy, not the original evidence. Compare the working copy with the approved version after saving.')
h('Challenge')
para('Separate the tasks: find instructions, edit the announcement, extract names, remove repetition, count workshop choices, compare schedules, and repair the timetable. Use intermediate files if a long pipeline is hard to reason about.')
para('A CHECK result can mean a missing file, wrong contents, or a changed original. Inspect the named file and the exact requirement. Ask for help before attempting to restore original evidence.', 'small')

page('COMMAND REFERENCE', 'Keep beside your terminal')
para('Examples are generic. Use the paths and values required by each exercise. Do not type the $ prompt or explanatory labels.', 'small')
table([
 ['Command or keys', 'Purpose'],
 ['history\nhistory 10', 'List remembered commands / show up to ten recent commands.'],
 ['history | grep -F "fragment"', 'Search command text. The search command itself may appear.'],
 ['Ctrl+R, then text\nCtrl+R again', 'Search history backwards / find an older match.'],
 ['Right Arrow / Enter / Ctrl+G', 'During history search: accept for editing / run / cancel.'],
 ['nano work/note.txt', 'Open an existing file or create a new text file.'],
 ['Ctrl+O, Enter / Ctrl+X', 'In nano: save and confirm filename / exit.'],
 ['less practice/handbook.txt', 'Read a file interactively without editing it.'],
 ['Space / b / g / G', 'In less: forward / backward / beginning / end.'],
 ['/word, Enter / n / N / q', 'In less: search / next / previous / quit.'],
 ['sort names.txt\nsort -nr scores.txt', 'Alphabetical text order / descending numerical order.'],
 ['sort names.txt | uniq\nsort names.txt | uniq -c', 'One line per distinct name / count each name.'],
 ['cut -d "|" -f 2 records.txt\ncut -d "|" -f 1,3 records.txt', 'Extract field 2 / fields 1 and 3 with a | separator.'],
 ['diff before.txt after.txt', 'Compare files; < belongs to before and > belongs to after.'],
 ['diff before.txt after.txt > changes.txt', 'Save a normal comparison to a separate file.'],
 ['command > work/result.txt\nfirst | second', 'Lab 1: save output (replace destination) / pass output onward.'],
 ], [250,W-250], compact=True)
para('Ctrl means Control on both Windows/Linux and Mac. Click the terminal before shortcuts. Commands run in Bash; nano and less have their own keys while open.', 'small')

def decorate(c, doc):
    width,height=doc.pagesize
    c.setStrokeColor(MINT); c.setLineWidth(3); c.line(42,height-30,width-42,height-30)
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(42,42,width-42,42)
    c.setFont('Body',8); c.setFillColor(GRAY)
    c.drawString(42,28,'TENSOR SCHOOL  |  INTRODUCTION TO SOFTWARE ENGINEERING  |  LAB 2')
    c.drawRightString(width-42,28,f'{doc.page} / 13')
    if doc.page > 13:
        raise RuntimeError('Booklet overflow: revise layout to fit the 13-page plan.')

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=(595.27,841.89), rightMargin=42,leftMargin=42,
    topMargin=48,bottomMargin=55,title='Lab 2 - Terminal Tools Experiment Book',author='Tensor School',
    subject='History, nano, less, sort, uniq, cut, and diff').build(story,onFirstPage=decorate,onLaterPages=decorate)
import re
from html import unescape
clean=[]
for block in md:
    if block.startswith('```'):
        clean.append(block)
    else:
        block=re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>',r'[\2](\1)',block)
        clean.append(unescape(re.sub(r'</?(?:u|b|i|br|font)\b[^>]*>','',block)))
TEXT.write_text('\n\n'.join(clean)+'\n',encoding='utf-8')
print(OUT)
