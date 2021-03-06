import numpy as np


def hangman(word):
  alpha = 'abcdefghijklmnopqrstuvwxyz'
  sofar = '_'*len(word)
  def show_guess(sofar): # Show the guess
    print('So far, computer has guessed: %s' %sofar)
    return
  def add_char(char, pos, sofar): # Add new character
    newsofar = ''
    for s in range(len(sofar)):
      if s != pos:
        newsofar = newsofar + sofar[s]
      else:
        newsofar = newsofar + char
    return newsofar
  while sofar != word:
    a = alpha[int(np.random.random(1)*26)]
    for char in range(len(sofar)):
      if sofar[char] == '_': # if it hasn't been guessed
        if word[char] == a:
          sofar = add_char(a, char, sofar)
          show_guess(sofar)
          break
    show_guess(sofar)
  return



#########################################################################


def rad_vs_somadist(geo):
  rad, dist = [], []
  pDF = PathDistanceFinder(geo, geo.soma)
  for s in geo.segments:
    rad.append(s.avgRadius)
    dist.append(pDF.distanceTo(s))
  return rad, dist
  

#########################################################################



def polar_bar():
  N = 20
  thetas = np.linspace(np.pi/2, np.pi, N)
  rads = np.random.random(N)
  width = np.pi/(2*N)
  #
  ax = plt.subplot(111, polar=True)
  bar = ax.bar(thetas, rads, width=width, bottom=4.)
  [b.set_facecolor('deeppink') for b in bar.patches]
  #[b.set_alpha(0.5) for b in bar.patches]
  [b.set_edgecolor('deeppink') for b in bar.patches]
  print(len(bar.patches))
  plt.show()
  return



def circular_hist(angles, labelsin, title=None):
  """
  # IMPORT DEPENDENCIES FROM TOP.
  """
  def to_radians(angs):
    return [i*np.pi/180. for i in angs]
  def r_bin(bins, target): # Return the target bin value, always start from below
    j = [i for i in bins]
    for i in j:
      if i > target:
        return i
  def angulize(angs, nbins=100): # Do everything for the plotting except plot
    if max(angs) > 2*np.pi:
      angs = to_radians(angs)
    rads, thetas_b = np.histogram(angs, bins=nbins)
    width = np.pi/(4*nbins)
    # Normalize hist height and center the bins
    rads = [i/max(rads) for i in rads]
    thetas = [(thetas_b[i]+thetas_b[i+1])/2. for i in range(len(thetas_b)-1)]
    q25, q75 = np.percentile(angs, [25, 75])
    b25, b75 = r_bin(thetas, q25), r_bin(thetas, q75)
    return rads, thetas, width, b25, b75
  # If it's just one object, plot it simply; else nest the lists
  if type(angles[0]) is not list:
    angles = [angles]
  # Else, create the nested plots
  colors = ['darkkhaki', 'royalblue', 'forestgreen','tomato']
  ax = plt.subplot(111, polar=True)
  for A in range(len(angles)):
    rads, thetas, width, t25, t75 = angulize(angles[A])
    bar = ax.bar(thetas, rads, width=width, bottom=2.+2*A)
    [b.set_facecolor(colors[A]) for b in bar.patches]
    [b.set_edgecolor(colors[A]) for b in bar.patches]
    iqr = ax.bar(np.linspace(t25, t75, 100), np.ones(100)*1.5, 
                 width=np.pi/(400), bottom=2.+2*A)
    [i.set_facecolor(colors[A]) for i in iqr.patches]
    [i.set_alpha(0.3) for i in iqr.patches]
    [i.set_linewidth(0.) for i in iqr.patches]
    mean = ax.bar(np.mean(angles), 1.5, width=np.pi/400, bottom=2.+2*A)
    med = ax.bar(np.median(angles), 1.25, width=np.pi/400, bottom=2.+2*A)
    k=['k','orange']
    for m in [med.patches[0], mean.patches[0]]:
      m.set_facecolor(k[[med.patches[0], mean.patches[0]].index(m)])
      m.set_linewidth(0.)
  # legend
  khaki_patch = mpatches.Patch(color='darkkhaki', 
                label=labelsin[0])
  patches = [khaki_patch]
  if len(angles) > 1:
    royal_patch = mpatches.Patch(color='royalblue', 
                  label=labelsin[1])
    patches.append(royal_patch)
  if len(angles) > 2:
    forest_patch = mpatches.Patch(color='forestgreen', 
                  label=labelsin[2])
    patches.append(forest_patch)
  if len(angles) > 3:
    lavender_patch = mpatches.Patch(color='tomato', 
                  label=labelsin[3])
    patches.append(lavender_patch)
  plt.legend(handles=patches, loc=4)
  # title
  if title:
    ax.set_title(title, fontsize=20)
  ax.set_yticklabels([])
  plt.show()
  return


##################################################################################

def fix_fuckup(infile, outfile):
  with open(infile, 'r') as fIn:
    for line in fIn: # assumes one long-ass line to be split into 4-col space-sep lines
      sline = line.split(' ')
      nline = []
      for s in sline:
        g = s.split('.')
        if len(g) > 2: # has more than 1 number, do the work
          dec0 = g[1][:6] # requires %.6f
          num1 = g[1][6:]
          nline.append(g[0]+'.'+dec0)
          nline.append(num1+'.'+g[2])
        else:
          nline.append(s)
      with open(outfile, 'w') as fOut:
        for n in range(int(len(nline)/4)): # skip first
          fOut.write('%f ' %float(nline[(n*4)]))
          fOut.write('%f ' %float(nline[(n*4)+1])) # 
          fOut.write('%f ' %float(nline[(n*4)+2]))
          fOut.write('%f ' %float(nline[(n*4)+3]))
          fOut.write('\n')
  return
  
############################################################################

edges, nodes = [], []
with open('new_hoc.hoc', 'r') as fIn:
  for line in fIn:
    if line:
      splitLine = line.split(None)
      if type(splitLine) is list:
        if splitLine[0] == 'connect':
          e1 = splitLine[1].split('[')[1].split(']')[0]
          if e1 not in nodes:
            nodes.append(e1)
          e1 = e1 + '.' + splitLine[1].split('(')[1].split(')')[0]
          e2 = splitLine[2].split('[')[1].split(']')[0]
          if e2 not in nodes:
            nodes.append(e2)
          e2 = e2 + '.' + splitLine[2].split('(')[1].split(')')[0]
          edges.append([e1, e2])



somapos = [[5.39,1.81,125.6], [157.82,0.9,130.9], [18.06,-6,30],
[20.91,3.97,124.04], [136.28,-2.56,98.6], [135.97,5.21,94.05], 
[141.5,2.72,3], [76.05,2.9,155], [82.21,-7.79,119],
[142.92,-12.91,55.2], [113.39,9.32,45.25], [142.55,-2.93,101],
[159.19,0.016,190], [60.77,-24.49,72.12], [161.54,0.065,203.52],
[98.014,1.68,238.58]]

soma_cells = ['LG','LG','LG','LG','LP','LP','LP','LP','PD','PD','PD','PD','GM','PD','GM','GM']


frac_dim=[1.1627001304,1.3001412706,1.191728541,1.2790871821,1.3250156116,1.3595518406,1.1348792355,1.2340712067,1.333833344,1.3390849673,1.3182916312,1.3117662475,1.2091119931,1.2903322362,1.1847130274,1.39]




############################################################################

def get_sub_lengths(infile):
  sublen = {}
  temp, f = None, None
  with open(infile, 'r') as fIn:
    for line in fIn:
      if line:
        splitLine = line.split(None)
        if splitLine[0] == 'file':
          sublen[f] = temp
          temp, f = [], splitLine[-1]
        else:
          pah = int(splitLine[-1])
          if pah not in temp:
            temp.append(int(splitLine[-1]))
  return sublen




total_wire = [20492.7,21997.68,26331.426,30048.63,27976.96,5083,41533.64,23660.896,17543.044,30399.49,26037.479,20325.15,18579.34,14774.77,15478.95,25036.36843]
xlcells = ['GM','LG','LG','GM','GM','PD','LP','LG','PD','PD','LG','PD','LP','LP','PD','LP']
num_subtrees = [32,25,15,35,37,10,23,19,6,15,33,2,12,6,3,20]
path_lengths = [1507,944.681,1105.2,6849,529.239,699.93,432.96,832.83,640.62,677.559159,842.117,1050.98,916.85716,365.041,700.75]
path_percent = [0.0685,0.0359,0.0368,0.2448,0.10411,0.01685,0.0183,0.04747,0.02107,0.02602,0.04143,0.0566,0.006206,0.02358,0.02799]


############################################################################

# sholl dict contains cellTypes, files, sholl_distances, sholl_counts, sholl_prods
def get_sholl_prods(sholl):
  # This function returns the sholl products by reversing the binning process
  for unit in range(len(sholl['files'])):
    prods = []
    for c in range(len(sholl['sholl_counts'][unit])):
      # dists.append(
      for mult in range(sholl['sholl_counts'][unit][c]):
        # Add the distance for all the count values
        prods.append(sholl['sholl_distances'][unit][c])
    sholl['sholl_prods'][unit] = prods
  return sholl
  


############################################################################

# for radius stuff
def single_ratios(rlist, skip=2):
  """
  Given a list, this assumes the format is parent1 daugh1a daught1b ...
  parentn daughtna daughtnb and returns a list daught1a/parent1 ...
  daughtnb/parentn. (Exactly 2/3 the size of input.)
  skip = len(str fields) that being each object (file, celltype)
  """
  outlist, count = [], 0
  if type(rlist[3]) is str: # First few items are usually str
    nlist = []
    for r in rlist:
      try:
        nlist.append(float(r))
      except:
        if str(r) == 'x':
          pass
        else:
          nlist.append(r)
    rlist = nlist
  rlist = [n for n in rlist if n != 0]
  for i in range(int((len(rlist)-skip)/3)):
    outlist.append(rlist[i*3+1+skip]/rlist[i*3+skip])
    outlist.append(rlist[i*3+2+skip]/rlist[i*3+skip])
  return outlist
  
  

def combined_ratios(rlist, skip=2):
  """
  Same as single_ratios but sums daughters; returns (daughters1a+b)/parent1.
  (Exactly 1/3 the size of input.)
  """
  outlist = []
  if type(rlist[3]) is str:
    nlist = []
    for r in rlist:
      try:
        nlist.append(float(r))
      except:
        if str(r) == 'x':
          pass
        else:
          nlist.append(r)
    rlist = nlist
  rlist = [n for n in rlist if n != 0]
  for i in range(int((len(rlist)-skip)/3)):
    outlist.append((rlist[i*3+1+skip]+rlist[i*3+2+skip])/rlist[i*3+skip])
  return outlist



def get_csv(csvfile):
  # Return list of csv row elements
  arr = []
  with open(csvfile, 'r') as cfile: # Assumes text, not binary
    creader = csv.reader(cfile) # Assumes csv
    for row in creader:
      nrow = []
      for i in row:
        try:
          nrow.append(float(i))
        except:
          nrow.append(i)
      arr.append(nrow)
  return arr


def pixel_div(x, y=None):
  # Get the 'average' pixel size to divide out.
  if y is None:
    y = x
  return 0.5*(np.mean([x,y]) + np.sqrt(2*x*y))


def div_radius(tips, divs, hand=False):
  # Divide non-string numbers by the divisor, len(tips)==len(divs)
  for t in range(len(tips)):
    for i in range(len(tips[t])):
      if hand is True:
        if type(tips[t][i]) is not str and tips[t][i] > 1: # Not binary
          tips[t][i] = tips[t][i]/divs[t]
      else: # Not hand
        if type(tips[t][i]) is not str:
          tips[t][i] = tips[t][i]/divs[t]
  return tips


def save_csv(tips, outfile, cols=None, rows=None):
  # Save a tips-like list of lists as a .csv
  if rows is not None:
    if cols is None:
      cols = range(max([len(t) for t in tips]))
    get = [[i] for i in rows]
    for k in cols:
      get[0].append(k)
    for t in range(len(tips)): # len(tips) = len(get)-1
      for c in tips[t]:
        get[t+1].append(c)
  else:
    get = tips
  with open(outfile, 'w') as fOut:
    for g in get:
      fOut.write(','.join([str(i) for i in g]))
      fOut.write('\n')
  print('%s written.' %outfile)
  return

    



############################################################################

# stochastic processes 
def invariant_TM(P, N=10):
  # Given a transition matrix P this calculates it's long-term behavior
  if type(P) != np.ndarray:
    try:
      P = np.array(P)
    except:
      print('Input must be numpy array'); return None
  B = P
  for i in range(N):
    P = P.dot(P)
  return P
  


def invariant_lefteig(P):
  """
  Gives the invariant transition matrix for an 2x2 matrix by left eigenvector.
  P = [[a, b],
       [c, d]]
  """
  a, b, c, d = P[0,0], P[0,1], P[1,0], P[1,1]
  return [c/(b+c), b/(b+c)]





#########################################################################
# fix torq histogram scaling

def rescale(values, scale=0.2):
  # Re-scale first bin just to show that the others aren't 0
  hist, edges = np.histogram(values, bins=100)
  hist[0] = hist[0]*scale
  new_vals = []
  centers = [(edges[i]+edges[i+1])/2. for i in range(len(edges)-1)]
  for b in range(len(hist)):
    for i in range(hist[b]):
      new_vals.append(centers[b])
  plt.hist(new_vals, bins=100)
  plt.show()
  return new_vals



for k in props.keys():
  print(k)
  for i in range(16):
    if k != 'files' and k != 'cellTypes':
      print(np.mean(props[k][i]), i)





############### congressional reporting ######################

def load_all(fname):
  """
  Load the state, party, last name and voting record of the senator.
  """
  def sep_party_name(thing):
    name = []
    if int(thing[0]) == 1: # Democrat
      party = 1
    elif int(thing[0]) == 2: # Republican
      party = 2
    else:
      party = 3 # Other
    for i in thing:
      try:
        int(i)
      except:
        name.append(i) # Only appends characters
    return ''.join(name), party
  states, names, parties, records = [], [], [], []
  with open(fname, 'r') as fIn:
    for line in fIn:
      if line:
        splitLine = line.split(None)
        if len(splitLine) < 4:
          print(line)
        else:
          states.append(splitLine[1][1:])
          n, p = sep_party_name(splitLine[2])
          names.append(n)
          parties.append(p)
          records.append([int(i) for i in splitLine[3]])
  return {'names': names, 'parties': parties, 'states': states, 'records': records}

  
def convert_record(record):
  """
  Pass the whole 100+ record list to this at once.
  Convert a 0-9 list of records (a list of lists len(senators)) to 
  yes(1)/no(0)/other(9).
  """
  newrec = [[] for i in record]
  for r in range(len(record)):
    temp = []
    # print(record[r])
    for i in record[r]:
      if i == 1:
        newrec[r].append(1)
      elif i == 6:
        newrec[r].append(0)
      else:
        newrec[r].append(9)
        # newrec[r].append(np.random.random(1)) # Eliminate spurious correlations
  return newrec


def get_correlation(record):
  """
  Pass the whole 100+ record list to this at once, returns 
  len(records) X len(records) correlation matrix.
  """
  corr = np.zeros([len(record), len(record)])
  for r in range(len(record)):
    for other in range(len(record)):
      temp = [sum([record[r][i]+record[other][i]]) for i in range(len(record[r]))]
      try:
        value = (float(temp.count(0))+float(temp.count(2))) / \
                (temp.count(0)+temp.count(2)+temp.count(1))
      except:
        value = 0
      corr[r][other] = value
  return corr


def corr_by_party(congress, party=None):
  """
  If party=None, congress must be a dict with 'parties' as a key. 
  Else, congress can be the record (list of lists) and party should
  be the list of parties (len(party)==len(congress)).
  1 = dem, 2 = repub, 3 = other
  """
  if party is None:
    if 'parties' in congress.keys():
      party = congress['parties']
    elif 'party' in congress.keys():
      party = congress['party']
    else:
      print('No party key found; pass the party list explicitly'); return None
  if type(congress) is dict:
    try:
      records = congress['records']
    except:
      records = congress['record']
  if len(records) != len(party):
    print('Records (%i) and party (%i) lists should be same length, but are not'
          %(len(records), len(party)))
    return None
  records_sorted = [x for (y,x) in sorted(zip(party, records))]
  corr = get_correlation(records_sorted)
  return corr


def save_matrix(mat, fname):
  """
  Save the corr matrix for plotting into R
  """
  with open(fname, 'w') as fOut:
    for row in mat:
      fOut.write(' '.join([str(i) for i in row]))
      fOut.write('\n')
  print('%s written' %fname)
  return
  
  

##########################################################################
# csv for wedding labels

def get_adds(fname)
  adds = []
  with open(fname, 'r') as fIn:
    for line in fIn:
      if line:
        adds.append(line.split(','))
  return adds



import string
def format_adds(adds):
  # Format the addresses
  exclude = list(set(string.punctuation))
  exclude.append(' ')
  def include(line, exclude):
    jine = [c for c in line if c not in exclude]
    if len(jine) == 0:
      return False
    else:
      return True
  #
  labels = []
  for a in adds[1:]:
    temp = []
    line1 = str('%s %s %s' %(a[2], a[3], a[4]))
    try:
      line2 = [i for i in [a[16], a[20], a[22]] if i != '']
    except:
      print(len(a), a)
      pass
    if len(line2) > 0:
      line2 = ' , '.join([str(i) for i in line2])
      line2 = '  &  ' + line2
    else:
      line2 = ''
    line3 = a[6]
    line4 = str('%s, %s  %s' %(a[8], a[9], a[10]))
    temp = [i for i in [line1, line2, line3, line4] if include(i, exclude)]
    labels.append(temp)
  return labels


def print_labels(labs, outfile=None):
  # Print the labels
  if outfile is None:
    print('Need an outfile name!')
    return None
  with open(outfile, 'w') as fOut:
    for l in labs:
      for i in l:
        fOut.write(i)
        fOut.write('\n')
      fOut.write('\n')
  print('%s written' %outfile)
  return


#############
# shrink the length-asymmetry vectors
def shrink_list(len_asym):
  new_orders, new_asyms = [], []
  for l in len_asym:
    new_asyms.append(l[0][::int(len(l[0])/1000)])
    new_orders.append(l[1][::int(len(l[1])/1000)])
  return new_asyms, new_orders


# somehow None order values are created (soma?); this cleans them
def clean_asym(la1, la2):
  for i in range(len(la1)):
    if la1[i].count(None) == 1:
      ind = la1[i].index(None)
      la1[i].pop(ind)
      la2[i].pop(ind)
    elif la1[i].count(None) > 1:
      for c in range(la1[i].count(None)):
        ind = la1[i].index(None)
        la1[i].pop(ind)
        la2[i].pop(ind)
  for i in range(len(la2)):
    if la2[i].count(None) == 1:
      ind = la2[i].index(None)
      la2[i].pop(ind)
      la1[i].pop(ind)
    elif la2[i].count(None) > 1:
      for c in range(la2[i].count(None)):
        ind = la2[i].index(None)
        la2[i].pop(ind)
        la1[i].pop(ind)
  return la1, la2


# Simple timing function
import datetime as dt
def start_time():
  return dt.datetime.now()
def end_time(then):
  print(dt.datetime.now() - then)
  return


# Simple attributes of an array
def min_max(arr):
  minn, maxx = np.inf, 0
  for i in arr:
    for j in i:
      if j > maxx:
        maxx = j
      if j < minn:
        minn = j
  print('Max: %f, Min: %f' %(float(maxx), float(minn)))
  return


#Get number of triplet/tuples in array
def num_of_triplets(arr):
  cnt = 0
  for i in arr:
      for j in i:
          if len(j) == 3:
              cnt = cnt + 1
  return cnt
  


###################
# subtree stuff

new_axs = [[601, 603, 604, 29451, 27749], [2848], [336], [3417, 5256, 3416, 7458], [6685, 6384, 1210, 5424], [1526], [7141], [7383, 4676, 3372]]
things = [['branch', 'branch','branch', 'seg', 'seg'], ['seg'], ['seg'], ['branch', 'branch', 'branch', 'branch'], ['seg', 'seg', 'seg', 'seg'], ['seg'], ['seg'], ['seg','seg','seg']]
gfils = [2, 1, 11, 3, 15, 8, 10, 0]

rand_stats, act_stats = [], []
sfs, sxs = [], []
for gil in range(len(gfils)):
  sf_, sx_ = subtree_filaments(geofiles[gfils[gil]], new_axs[gil], things[gil], True)
  loc_ = subtree_tips(geofiles[gfils[gil]], sx_)
  sts_, _ = randomize_subtrees(loc_, 2000, 1)
  rand_stats.append(sts_)
  stats_ = subtree_statistics(loc_)
  act_stats.append(stats_)

# From tips_locations json, get all subtree stats:
rand_stats, samps = [], []
for l in tips_locs['locations']:
  try:
    stt, smp = randomize_subtrees(l, 2000,1)
  except:
    try:
      stt, smp = randomize_subtrees(l, 500, 1)
    except:
      try:
        stt, smp = randomize_subtrees(l, 100, 1)
      except:
        stt, smp = randomize_subtrees(l, 50, 1)
  rand_stats.append(stt)
  samps.append(smp)


# Print the means of each group of keys

def condition_by_name(labels, arr, arr2=None, arr3=None):
  # sort by common labels in order so same types show up next to one another
  unique_labels = np.unique([i for i in labels])
  order = []
  for i in unique_labels:
    for x in range(len(labels)):
      if labels[x] == i:
        order.append(x)
  new_labels = [labels[j] for j in order]
  new_arr = [arr[j] for j in order]
  if arr2:
    new_arr2 = [arr2[j] for j in order]
  if arr3:
    new_arr3 = [arr3[j] for j in order]
    return new_labels, new_arr, new_arr2, new_arr3
  if arr2:
    return new_labels, new_arr, new_arr2
  return new_labels, new_arr


def dict_means(data):
  """
  Returns the means +/- std for the keys in a dict by cell type
  """
  for k in [key for key in data.keys() if key not in ['files', 'cellTypes']]:
    labs, vals = condition_by_name(data['cellTypes'], data[k])
    print(k, [labs[0], labs[4], labs[8], labs[12]])
    for u in range(4):
      print(np.mean([np.mean([vals[u*4+i]]) for i in range(4)]),
            np.mean([np.std([vals[u*4+i]]) for i in range(4)]))
  return




bat = [[233.97541464398489, 320.43812381755367, 174.44805831951726, 209.43501860355963], [233.97541464398489, 320.43812381755367, 174.44805831951726, 209.43501860355963], [427.43688192076525, 462.10622919034574, 154.14740882414463, 187.25348006474422], [427.43688192076525, 462.10622919034574, 154.14740882414463, 187.25348006474422], [314.61810538029704, 393.5912279530362, 179.89267296624217, 216.64999370042455], [314.61810538029704, 393.5912279530362, 179.89267296624217, 216.64999370042455], [165.76553886579845, 356.8670537267941, 74.646490127909928, 203.13662098320117], [165.76553886579845, 356.8670537267941, 74.646490127909928, 203.13662098320117], [165.76553886579845, 356.8670537267941, 74.646490127909928, 203.13662098320117], [165.76553886579845, 356.8670537267941, 74.646490127909928, 203.13662098320117]]


batch = [[1, '/home/alex/data/adriane/skeletons/diams_targets/878_061_skeleton_targetsAOdiametersxyz.002.nml'],
[2, '/home/alex/data/adriane/skeletons/diams_targets/878_043_targetsAO.diametersxyz.001.nml'],
[3, '/home/alex/data/adriane/skeletons/diams_targets/878_065_skeleton_targetsAOdiametersxyz.003.nml'],
[4, '/home/alex/data/adriane/skeletons/diams_targets/878_049_targetsAO.diametersxyz.001.nml'],
[5, '/home/alex/data/adriane/skeletons/diams_targets/878_057_targetsAOdiametersxyz.001.nml'],
[6, '/home/alex/data/adriane/skeletons/diams_targets/878_045_targetsAOdiametersxyz.nml'],
[8, '/home/alex/data/adriane/skeletons/diams_targets/878_053_targetsAOdiametersxyz.001.nml'],
[9, '/home/alex/data/adriane/skeletons/diams_targets/878_056_targetsAOdiametersxyz.001.nml'],
[10, '/home/alex/data/adriane/skeletons/diams_targets/878_041_targetsAOdiametersxyz.005.nml'],
[12, '/home/alex/data/adriane/skeletons/diams_targets/878_062_skeleton_targetsAOdiametersxyz.002.nml']]


def headrow(inarow=3, N=1000, show=False):
  # How long does it take to get 3 heads in a row?
  def cnt(trac):
    c = 0
    for u in trac[::-1]:
      if u == 1:
        c = c + 1
      else:
        return c
    return c
  traces = []
  for n in range(N):
    temp = [np.random.randint(0,2) for i in range(3)]
    while sum(temp[-inarow:]) < inarow: # 1=heads, so sum(last 3) should be 1
      temp.append(np.random.randint(0,2))
    traces.append(temp)
  print('Avg time to %i heads: %.2f' %(inarow, np.mean([len(u) for u in traces])))
  print('Median time to %i heads: %.2f' %(inarow, np.median([len(u) for u in traces])))
  if show:
    for tr in traces[:100]:
      plt.plot([cnt(tr[i:i+inarow]) for i in range(len(tr)-inarow+1)], color='black', alpha=0.1)
    hist, b_e = np.histogram([len(t) for t in traces], bins=40)
    b_c = 0.5*(b_e[:-1]+b_e[1:])
    plt.bar(b_c, [inarow*h/max(hist) for h in hist], width=b_e[1]-b_e[0], 
            color='blue', alpha=0.7, edgecolor='white')
    plt.show()
  return

#
0 878_058_GM_scaled
1 878_061_GM_scaled
2 878_043_GM_scaled
3 878_065_GM_scaled
4 878_049_GM_firstpass_scaled
5 878_057_GM_firstpass_scaled
6 878_045_GM_scaled
7 878_063_GM_scaled
8 878_053_GM_scaled
9 878_056_GM_scaled
10 878_041_GM_firstpass_scaled
11 878_064_GM_scaled
12 878_062_GM_scaled


###################### savitzky-golay ############################
def s_golay(x, winsize, degree):
  # Simple Savitzky-Golay filter, inspired by matlab
  assert winsize % 1 == 0, 'winsize must be int!'
  assert winsize % 2 == 1, 'winsize must be odd!'
  assert winsize > 0, 'winsize must be positive!'
  assert winsize > degree + 2, 'winsize must be > (degree+2)'
  
  # Condition data and establish convolution coefficients
  r_degree = range(degree+1)
  halfwin = int((winsize-1)/2)
  convmat = np.mat([ [k**i for i in r_degree]
                    for k in range(-halfwin, halfwin+1) ])
  m = np.linalg.pinv(convmat).A[0]
  
  # Stretch the signal at extrema so that computation can continue
  start = np.interp(np.linspace(0.5, 0.5*2*halfwin, 2*halfwin),
                    np.linspace(0.,halfwin, halfwin), x[0:halfwin])
  end = np.interp(np.linspace(0.5, 0.5*2*halfwin, 2*halfwin),
                  np.linspace(0.,halfwin, halfwin), x[-(halfwin):])
  x = np.concatenate((start, x, end))

  result = np.convolve(m[::-1], x, mode='valid')
  # In case it's too long, shrink it
  pad = int((len(x)-len(result))/2)
  if pad > 0:
    return result[pad-1:-pad]
  return result

#


def read_matfile(fname, sep=' '):
  arr = []
  with open(fname, 'r') as F:
    for line in F:
      temp_ = []
      for u in line.strip().split(sep):
        try:
          temp_.append(float(u))
        except:
          pass
      arr.append(temp_)
  return arr



def norm_sholl(counts):
  import scipy.stats as stats
  x = list(range(len(counts)))
  newcnt = []
  for c in range(len(counts)):
    temp = [x[c] for i in range(int(counts[c]))]
    for t in temp:
      newcnt.append(t)
  return float(stats.mode(newcnt)[0])/float(len(counts))


def combine_dict(big_one, small_one, by='files'):
  # Add keys from small one that match big one if that key isn't in big one
  for k in small_one.keys():
    if k not in big_one.keys():
      big_one[k] = []
      # Line up the file names by ###_### notebook
      for fil1 in big_one[by]: # This is the order that matters
        for fil2 in small_one[by]:
          seek = '_'.join(fil2.split('_')[:2])
          print('looking for ' +seek)
          if seek in fil1: # Find the matching small
            big_one[k].append(small_one[k][small_one[by].index(fil2)]) # Add that one
  return big_one


  
def num_nodes(geofile):
  count = 0
  with open(geofile, 'r') as fIn:
    for line in fIn:
      if line:
        if 'pt3dadd' in line:
          count += 1
  print(count)
  return count



def intraclass_corrlation(V, groups, collapsed=True):
  """
  Simple intraclass correlation where a V= list of lists, or a list of floats,
  and len(labelsin) == len(V). Can pass cols of a df if collapsed=False.
  (within group variance)^2 / ( (within group var)^2 + (between all sample var)^2 )
  0 = individuals are source of variab., 1 = groups are source of variab.
  """
  import scipy.stats as stats
  if not collapsed:
    V = [[i] for i in V]
  colors = ['darkkhaki', 'royalblue', 'forestgreen','tomato']
  var = [np.var(i) for i in V]
  uniq = list(set(groups))
  v_sort = [[] for u in uniq] # Make a blank list, preparing for IC
  v_means = [[] for u in uniq] # v_means is a list of list of means for each cell of each type
  v_var, v_skew, v_kurt = [[] for u in uniq], [[] for u in uniq], [[] for u in uniq]
  for v in range(len(V)):
    i = uniq.index(groups[v])
    v_sort[i].append(V[v])
    v_means[i].append(np.mean(V[v]))
    v_var[i].append(np.var(V[v]))
  # ic = var_between^2 / (var_between^2 + var_within^2)  
  ic = []
  for v in range(len(uniq)):
    I = np.var(v_means[v])**2 / \
        (np.var(v_means[v])**2 + sum([np.var(i) for i in v_sort[v]])**2)
    ic.append([I])
  print(ic)
  group_means = [np.mean(k) for k in v_means] # group_means are the master means (only 4)
  master_ic = np.var(group_means)**2 / \
              (np.var(group_means)**2 + sum([np.var(i) for i in v_means])**2)
  print('Master IC for this set: %.5f' %master_ic)
  return ic



















