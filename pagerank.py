import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    dic = dict()
    if len(corpus[page]) == 0:
        for p in corpus.keys():
            dic[p] = 1/len(corpus.keys())
    else:
        for p in corpus.keys():
            if p in corpus[page]:
                dic[p] = (1/(len(corpus[page])))*damping_factor + (1-damping_factor)/len(corpus.keys())
            else:
                dic[p] = (1-damping_factor)/len(corpus.keys())
    return dic
    


    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    '''raise NotImplementedError'''
 

def sample_pagerank(corpus, damping_factor, n):
    
    rank = dict()
    for i in corpus.keys():
        rank[i] = 0
    x = random.choice(list(corpus.keys()))
    transition = transition_model(corpus,x,damping_factor)
    for i in range(n):
        choice = random.choices(list(corpus.keys()),weights = list(transition.values()),k=1)[0]
        rank[choice] +=1
        transition = transition_model(corpus, choice, damping_factor )
        
    for i in rank.keys():
        rank[i] = rank[i]/n
    

    return rank
   

   

    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    rank = dict()
    for i in corpus.keys():
        rank[i] = 1/len(corpus.keys())
    def pr(page):
            sum = 0
            if len(corpus[page]) == 0:
                for i in corpus.keys():
                    sum += rank[i]/len(corpus[i])
                pr = (1-damping_factor)/len(corpus.keys()) + damping_factor*sum
                return pr
            else:
                for i in corpus.keys():
                    if page in corpus[i]:
                        sum += rank[i]/len(corpus[i])
                pr = (1-damping_factor)/len(corpus.keys()) + damping_factor*sum
                return pr
    while(True):
        prvs = list()
        news = list()      
        for i in corpus.keys():
            prv = rank[i]
            prvs.append(prv)
            rank[i] = pr(i)
            news.append(rank[i])
        diff = [abs(prvs[i]-news[i]) for i in range(len(prvs))]
        if(False not in [i<=0.001 for i in diff]):
            break
    
    return rank

        
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
