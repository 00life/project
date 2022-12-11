import pickle, random, os, time

period_info = [(1, 'H', 'Hydrogen'), (2, 'He', 'Helium'), (3, 'Li', 'Lithium'), (4, 'Be', 'Beryllium'), (5, 'B', 'Boron'), (6, 'C', 'Carbon'), (7, 'N', 'Nitrogen'), (8, 'O', 'Oxygen'), (9, 'F', 'Fluorine'), (10, 'Ne', 'Neon'), (11, 'Na', 'Sodium'), (12, 'Mg', 'Magnesium'), (13, 'Al', 'Aluminum'), (14, 'Si', 'Silicon'), (15, 'P', 'Phosphorus'), (16, 'S', 'Sulfur'), (17, 'Cl', 'Chlorine'), (18, 'Ar', 'Argon'), (19, 'K', 'Potassium'), (20, 'Ca', 'Calcium'), (21, 'Sc', 'Scandium'), (22, 'Ti', 'Titanium'), (23, 'V', 'Vanadium'), (24, 'Cr', 'Chromium'), (25, 'Mn', 'Manganese'), (26, 'Fe', 'Iron'), (27, 'Co', 'Cobalt'), (28, 'Ni', 'Nickel'), (29, 'Cu', 'Copper'), (30, 'Zn', 'Zinc'), (31, 'Ga', 'Gallium'), (32, 'Ge', 'Germanium'), (33, 'As', 'Arsenic'), (34, 'Se', 'Selenium'), (35, 'Br', 'Bromine'), (36, 'Kr', 'Krypton'), (37, 'Rb', 'Rubidium'), (38, 'Sr', 'Strontium'), (39, 'Y', 'Yttrium'), (40, 'Zr', 'Zirconium'), (41, 'Nb', 'Niobium'), (42, 'Mo', 'Molybdenum'), (43, 'Tc', 'Technetium'), (44, 'Ru', 'Ruthenium'), (45, 'Rh', 'Rhodium'), (46, 'Pd', 'Palladium'), (47, 'Ag', 'Silver'), (48, 'Cd', 'Cadmium'), (49, 'In', 'Indium'), 
(50, 'Sn', 'Tin'), (51, 'Sb', 'Antimony'), (52, 'Te', 'Tellurium'), (53, 'I', 'Iodine'), (54, 'Xe', 'Xenon'), (55, 'Cs', 'Cesium'), (56, 'Ba', 'Barium'), (57, 'La', 'Lanthanum'), (58, 'Ce', 'Cerium'), (59, 'Pr', 'Praseodymium'), (60, 'Nd', 'Neodymium'), (61, 'Pm', 'Promethium'), (62, 'Sm', 'Samarium'), (63, 'Eu', 'Europium'), (64, 'Gd', 'Gadolinium'), (65, 'Tb', 'Terbium'), (66, 'Dy', 'Dysprosium'), (67, 'Ho', 'Holmium'), (68, 'Er', 'Erbium'), (69, 'Tm', 'Thulium'), (70, 'Yb', 'Ytterbium'), (71, 'Lu', 'Lutetium'), (72, 'Hf', 'Hafnium'), (73, 'Ta', 'Tantalum'), (74, 'W', 'Tungsten'), (75, 'Re', 'Rhenium'), (76, 'Os', 'Osmium'), (77, 'Ir', 'Iridium'), (78, 'Pt', 'Platinum'), (79, 'Au', 'Gold'), (80, 'Hg', 'Mercury'), (81, 'Tl', 'Thallium'), (82, 'Pb', 'Lead'), (83, 'Bi', 'Bismuth'), (84, 'Po', 'Polonium'), (85, 'At', 'Astatine'), (86, 'Rn', 'Radon'), (87, 'Fr', 'Francium'), (88, 'Ra', 'Radium'), (89, 'Ac', 'Actinium'), (90, 'Th', 'Thorium'), (91, 'Pa', 'Protactinium'), (92, 'U', 'Uranium'), (93, 'Np', 'Neptunium'), (94, 'Pu', 'Plutonium'), (95, 'Am', 'Americium'), (96, 'Cm', 'Curium'), (97, 'Bk', 'Berkelium'), (98, 'Cf', 'Californium'), (99, 'Es', 'Einsteinium'), (100, 'Fm', 'Fermium'), (101, 'Md', 'Mendelevium'), (102, 'No', 'Nobelium'), (103, 'Lr', 'Lawrencium'), (104, 'Rf', 
'Rutherfordium'), (105, 'Db', 'Dubnium'), (106, 'Sg', 'Seaborgium'), (107, 'Bh', 'Bohrium'), (108, 'Hs', 'Hassium'), (109, 'Mt', 'Meitnerium'), (110, 'Ds', 'Darmstadtium'), (111, 'Rg', 'Roentgenium'), (112, 'Cn', 'Copernicium'), (113, 'Nh', 'Nihonium'), (114, 'Fl', 'Flerovium'), (115, 'Mc', 'Moscovium'), (116, 'Lv', 'Livermorium'), (117, 'Ts', 'Tennessine'), (118, 'Og', 'Oganesson')]

current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dat_path = os.path.join(current_dir,'static','dat','prev.dat')
time_path = os.path.join(current_dir,'static','dat','time.dat')
verbose = True

def chem_quest(atomic_start=1, atomic_end=36, questions=18):

    # Example: periodic_data_set = {(1,'H','Hyrogen),...} # Random Elements for questions
    # Example: random_012_list = [(0, 2), (2, 1), (1, 0)...] # Random tuples for questions
    perioic_data_set, random_012_list = set(), []
   
    # Generating random data_sets (eg. (1,'H','Hyrogen)) and Q&A for each set (eg.(0, 2))
    while True:
        try:
            if len(perioic_data_set) == questions and len(random_012_list) == questions: break
            if len(perioic_data_set) < questions:
                rand = random.randint(atomic_start-1,atomic_end-1)
                perioic_data_set.add(period_info[rand])
            if len(random_012_list) < questions:
                rand1, rand2 = random.randint(0,2),random.randint(0,2)
                random_012_list.append((rand1,rand2)) if rand1 != rand2 else ""
        except Exception: pass
   
    question_answer_list = []
    key = {0:'ATOMIC NUMBER',1:'ELEMENT SYMBOL',2:'ELEMENT NAME'}
    for i, period in enumerate(perioic_data_set):
        que_ans, given = random_012_list[i]
        question = f"What's its {key[que_ans]}?"
        question_answer_list.append((i+1,question, period[que_ans], period[given], key[given], key[que_ans]))
    
    # with open(dat_path,'wb') as fin:
    #     pickle.dump(question_answer_list,fin)

    # Saving the current time for used in evaluate()
    # with open(time_path,'wb') as fin:
    #     pickle.dump(time.time(),fin)
    
    return question_answer_list
    # Example: [(1, 'What's its ELEMENT NAME?', 'Hydrogen', 'H', 'ELEMENT SYMBOL', 'ELEMENT NAME'),...]


def evaluate(get_ans, ques, ans, given, num):

    boolean = all([True if ans == '' else False for ans in get_ans])
    
    wrong = []
    if not boolean:
        for i in range(len(get_ans)):
            try:
                if get_ans[i].lower() != str(ans[i]).lower():
                    wrong.append((num[i],given[i],ques[i],get_ans[i],ans[i]))
            except:pass
        score = [ len(get_ans) - len(wrong), len(get_ans) ]
 
        return (wrong,score)
    return([],[])

if __name__ == "__main__":
    a = chem_quest()
    print(a)
    #evaluate([])
   
    


    

    