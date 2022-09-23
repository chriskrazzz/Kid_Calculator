
fin = open("growth_rates.txt")

## dictionary layout: key = character name
# hp, str, mag, skl, spd, lck, def, res
char = dict()
moms = []
dads = []
kids = []
avas = [] #avatar sexuals

for line in fin:
    line = line.strip()
    line = line.split()
    key = ''
    i = 0
    for word in line:
        if i == 0:
            key = word
            char[key] = []
            i += 1
        elif i == 9:
            if (word == 'f') or (word == 'b'):
                moms.append(key)
            if (word == 'm') or (word == 'b'):
                dads.append(key)
            elif word == 'c':
                kids.append(key)
            elif word == 's':
                avas.append(key)
        else:
            char[key].append(int(word))
            i += 1


def make_kid(mom, kid, boon = None, lib = char, boons = None):
            #mom refers to parent who gives stats, so any male who marries
            #female corrin/azura also
    mom = mom.capitalize()
    kid = kid.capitalize()

    momstats = lib[mom]
    kidstats = lib[kid]
    efstats = [mom, kid]

    if (mom == 'Avatar') and boon and boons:
        momstats += boons[boon]
    
    for i in range(len(momstats)):
        efstats.append((momstats[i] + kidstats[i]) / 2)
        if efstats[-1] == int(efstats[-1]):
            efstats[-1] = int(efstats[-1])
    return efstats

def run_all(boon = None, lib = char, moms = moms, dads = dads, kids = kids,
            avas = avas, boons = None):
    result = []
    
    for kid in kids:
        if kid == 'Shigure':
            for dad in dads:
                result.append(make_kid(dad, kid, boon = boon, lib = lib))
                
        elif kid == 'Kana':
            # the kids are not really done yet, since their stats depend on
            # the stats of their parents
            for mom in moms:
                if mom == 'Avatar':
                    continue
                result.append(make_kid(mom, kid, lib = lib))
                
            for dad in dads:
                if dad == 'Avatar':
                    continue
                result.append(make_kid(dad, kid, lib = lib))
                
            for ava in avas:
                result.append(make_kid(ava, kid, lib = lib))
                
            for kid2 in kids:
                if kid2 == 'Kana':
                    continue
                result.append(make_kid(kid2, kid, lib = lib))
                
        else:     
            for mom in moms:
                result.append(make_kid(mom, kid, boon = boon, lib = lib,
                              boons = boons))
    return result

     
data = run_all() 
                
def printkid(kid, mom, data):
    mom = mom.capitalize()
    kid = kid.capitalize()
    found = False
    
    for result in data:
        if result[0] == mom and result[1] == kid:
            print(f"If {mom} is the parent of {kid}, then this will be their"+
                  f" individual growth:\n HP:  {result[2]}\n Str: {result[3]}"+
                  f"\n Mag: {result[4]}\n Skl: {result[5]}\n Spd: {result[6]}"+
                  f"\n Lck: {result[7]}\n Def: {result[8]}\n Res: {result[9]}"+
                  f"\n Total: {sum(result[2:10])}")
            found = True

    if not found:
        print(f'Could not find information about {kid} with {mom} as parent.')

## initializing stat dictionary to get the index with given stat name
stats = dict()
stats["HP"] = 0
stats["Str"] = 1
stats["Mag"] = 2
stats["Skl"] = 3
stats["Spd"] = 4
stats["Lck"] = 5
stats["Def"] = 6
stats["Res"] = 7


def find_max(kid, data, *args): #accepts HP, Str, Mag..., and Tot for total
    kid = kid.capitalize()
    if kid not in kids:
        print(f"{kid} not in dataset")
        return None

    
    todo = [*args]

    mult = [0, 0, 0, 0, 0, 0, 0, 0]
    endstr = ''
    j = 0
    for stat in todo:
        check = stat.lower()
        if check == "hp":
            stat = "HP"
        else:
            stat = stat.capitalize()
            
        if stat == "Tot":
            for i in range(len(mult)):
                mult[i] += 1
        else:
            try:
                mult[stats[stat]] += 1
            except KeyError:
                print(f"{stat} does not exist, try again")
                return None

        if j == 0:
            endstr += stat
            j += 1
        else:
            endstr += ', ' + stat
    
    result = [] 
    high = 0

    for line in data:
        if line[1] == kid:
            score = 0
            for i, stat in enumerate(line[2:10]):
                score += stat * mult[i]
            if score == high:
                result.append(line)
            if score > high:
                high = score
                result = [line]

    for i, line in enumerate(result):
        print(f"{result[i][0]} was found to be (one of) the parent(s) who"+
              f" gives {kid} the highest:\n"
                + endstr +'.')
        printkid(kid, result[i][0], data)
        print('\n')
    

find_max("shigure", data, "mag", "spd", "tot")

