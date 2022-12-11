import os
from pprint import pprint

PATH_CWD = os.path.dirname(os.path.realpath(__file__))

testPath = os.path.join(PATH_CWD,'test.txt')
testPath2 = os.path.join(PATH_CWD,'test2.txt')

with open(testPath,'r') as fout:
    content = fout.read()

contentList = content.split('\n')
newStringCont = []
for cont in contentList:
    num = cont[0:5]

    try: num = int(num)
    except:pass

    if isinstance(num,int):
        repl = cont[5:].replace('You','He/she').replace('Student','He/she').replace('their','his/her')
        repl = repl.replace('your','his/her').replace('Coop student','He/she').replace('usually arguments','usually uses arguments')
        repl = repl.replace('Needs','He/she needs').replace('Should','He/she should').replace('Class participation','His/her class participation')
        repl = repl.replace('Demonstrates','He/she demonstrates').replace('Sometimes','He/she sometimes')
        repl = repl.replace('Infrequently','He/she infrequently').replace('Usually','He/she usually')
        repl = repl.replace('Routinely', 'He/she routinely').replace('Applies','He/she applies')
        repl = repl.replace('Uses','He/she uses').replace('Communicates','He/she communicates')
        repl = repl.replace('Analyses','He/she analyses').replace('Assesses','He/she Assesses').replace('Class behaviour','His/her class behaviour')
        repl = repl.replace('Extends','He/she extends').replace('you repeat','he/she repeat').replace('Must prepare','He/she must prepare')
        repl = repl.replace('you consider','he/she consider').replace('you continue','he/she continue')
        repl = repl.replace('Participates','He/she participates').replace('Takes initiative','He/she takes initiative')
        repl = repl.replace('Approaches','He/she Approaches').replace('Applies','He/she applies').replace('Makes','He/she makes')
        repl = repl.replace('Displays','He/she Displays').replace('Maintains','He/she maintains').replace('Make better use','He/she should make better use')
        repl = repl.replace('Actively','He/she actively').replace('Attempts','He/she attempts').replace('Shows','He/she shows')
        repl = repl.replace('Follows','He/she follows').replace('Has a','He/she has a').replace('Consistently','He/she consistently')
        repl = repl.replace('Has difficulty','He/she has difficulty').replace('Punctuality','His/her punctuality')
        repl = repl.replace('Try to','He/she should try to').replace('improve results','improve his/her results')
        repl = repl.replace('Solves','He/she solves').replace('Selects','He/she selects').replace('Performs','He/she performs')
        repl = repl.replace('Recognizes','He/she recognizes').replace('Recommend you','Recommend he/she').replace('Take studies','He/she should take studies')
        repl = repl.replace('Considerable application','He/she has considerable application').replace('Moderate application','He/she has moderate application')
        repl = repl.replace('Limited application','He/she has limited application').replace('Infrequent','He/she has infrequent')
        repl = repl.replace('Catch up','He/she should catch up').replace('Use agenda','He/she should used agenda')
        repl = repl.replace('Complete assignments','He/she should complete assignments').replace('Improve notebook','He/she should improve notebook')
        repl = repl.replace('Take more care','He/she should take more care').replace('Transfers','He/she transfers')
        repl = repl.replace('Monitor the','He/she should monitor the').replace('Focus on','He/she should focus on')
        repl = repl.replace('Must do','He/she must do').replace('Seek','He/she should seek').replace('Read more','He/she should read more')
        repl = repl.replace('Writing skills','His/her writing skills').replace('Note taking','His/her note taking')
        repl = repl.replace('Work','His/her work').replace('Must strive','He/she must strive').replace('reflected in','reflected in his/her')
        repl = repl.replace('Daily attendance','His/her daily attendance').replace('Homework must','His/her homework must')
        repl = repl.replace('Co-operation with','His/her co-operation with').replace('Organizational','His/her organizational')
        repl = repl.replace('Learn','He/she should Learn').replace('Writes','He/she writes').replace('Reads','He/she reads')
        repl = repl.replace('Analyzes','He/she analyzes').replace('Speaks','He/she speaks').replace('Edits','He/she edits')
        repl = repl.replace('Writing','His/her writing').replace('Drill','He/she should drill').replace('Knowledge','His/her knowledge')
        repl = repl.replace('Practise','He/she should practice').replace('Study','He/she should study').replace('Improve Time','He/she should Improve Time')
        repl = repl.replace('Improve','He/she should improve').replace('Review','He/she should review').replace('Listen','He/she should listen')
        repl = repl.replace('Organize','He/she should organize').replace('Check','He/she should check').replace('Ask for','He/she should ask for')
        repl = repl.replace('Take advantage','He/she should take advantage').replace('Check','He/she should check').replace('Use time','He/she should use time')
        repl = repl.replace('Practice','He/she should practice').replace('Prepare','He/she should prepare').replace('Consult','He/she should cpnsult')
        repl = repl.replace('Pursue','He/she should pursue').replace('Remains','He/she remains').replace('Takes','He/she takes')
        repl = repl.replace('Apply','He/she should apply').replace('Must','He/she must').replace('Become','He/she should become')
        repl = repl.replace('Set','He/she should set').replace('Stay','He/she should stay').replace('Continue','He/she should continue')
        repl = repl.replace('Has','He/she has').replace('Stay','He/she should stay').replace('Consider', 'He/she should consider')
        repl = repl.strip()

        newCont = '{'+f'N({str(num)})N S(Religion)S G(Next)G' +'} '+f'{repl}'
        
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' few ')!=-1 or newCont.find(' some ' )!=-1 or newCont.find(' most ')!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' constant ')!=-1 or newCont.find(' minimal ' )!=-1 or newCont.find(' limited ')!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' moderate ')!=-1 or newCont.find(' considerable ' )!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' accurately ')!=-1 or newCont.find(' usually uses correct ' )!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' solves complex ')!=-1 or newCont.find(' relating to unfamiliar ' )!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' accurately.')!=-1 or newCont.find(' relating to unfamiliar ' )!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' good understanding ')!=-1 or newCont.find(' relating to unfamiliar ' )!=-1 else newCont
        newCont = newCont.replace(')S G(',')S M(100)M m(80)m G(') if newCont.find(' high degree ')!=-1 or newCont.find(' relating to unfamiliar ' )!=-1 else newCont

        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' few ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' some ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(79)M').replace('m(80)m','m(70)m') if newCont.find(' most ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' sometimes.')!=-1 else newCont

        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' constant ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' some ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(79)M').replace('m(80)m','m(70)m') if newCont.find(' minimal ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' inconsistent ')!=-1 else newCont

        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' simple ' )!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' Limited' )!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' limited' )!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' moderate ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(79)M').replace('m(80)m','m(70)m') if newCont.find(' good understanding ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' Infrequent ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(69)M').replace('m(80)m','m(60)m') if newCont.find(' sometimes makes ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' needs to work ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent pronunciation errors ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent errors ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent support.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' many errors.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' many pronunciation errors.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' many errors ')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent pronunciation errors.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent errors.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(59)M').replace('m(80)m','m(50)m') if newCont.find(' frequent errors.')!=-1 else newCont
        newCont = newCont.replace('M(100)M','M(79)M').replace('m(80)m','m(70)m') if newCont.find(' considerable ')!=-1 else newCont
       
        
        newStringCont.append(newCont)

newNew = '\n'.join(newStringCont)
print(newNew)
# with open(testPath2,'w') as fin:
#     fin.write(newNew)
