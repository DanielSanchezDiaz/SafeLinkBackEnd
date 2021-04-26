# Script which loads all found homophones
# creates a dictionary of them and then searches
# popular domain names for the presense of them
import os
import sys
import socket
import random
import itertools
import time
import tldextract


class Homophones:

    def __init__(self, homophones_f, wordlist_f):
        self.HP_MIN_LENGTH = 2
        self.WORD_MIN_LENGTH = 2
        self.MAX_TRY_SECS = 30

        self.load_homophones(homophones_f)
        self.load_wordlists(wordlist_f)

    # Unique(list)
    # Gotten from http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    @staticmethod
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if x not in seen and not seen_add(x)]

    @staticmethod
    def all_perms(elements):
        if len(elements) <= 1:
            yield elements
        else:
            for perm in Homophones.all_perms(elements[1:]):
                for i in range(len(elements)):
                    # nb elements[0:1] works in both string and list contexts
                    yield perm[:i] + elements[0:1] + perm[i:]

    @staticmethod
    def all_combinations(iterable):
        combs = []

        for s in range(len(iterable) + 1):
            for comb in itertools.permutations(iterable, s):
                yield comb
                # combs.append(list(comb))

    def load_wordlists(self, wl_path):
        wordlist = []
        f = open(wl_path, "r")
        bl_chars = ['&', '/', '\'']
        whitelist = ['3d', 'xxx', '1st', '2nd', '3rd',
                     '4th', '5th', '6th', '7th', '8th', '9th', '0th']

        for word in f:
            word = word.strip()

            # Remove words that are either too short or that include blacklisted characters
            if len([c for c in bl_chars if c in word]) > 0:
                continue
            if len(word) < self.WORD_MIN_LENGTH and word.isdigit() == False:
                continue

            # Remove words that have no vowels (weird acronyms) [Including Y]
            vowels = "aeiuoy"
            if len([v for v in vowels if v in word]) == 0 and word.isdigit() == False and word not in whitelist:
                continue

            wordlist.append(word)

        f.close()
        self.wordlist = set(wordlist)

    def load_homophones(self, data_path):
        # First from homophone.com
        h_dirs = ["homophone.com", "wikipedia"]
        homophones = {}
        for h_dir in h_dirs:

            f_names = os.listdir("%s/%s/txt/" % (data_path, h_dir))
            for f_name in f_names:
                # print ("Parsing %s" % f_name)

                if f_name == ".svn":
                    continue

                f = open("%s/%s/txt/%s" % (data_path, h_dir, f_name))
                for line in f:

                    # Handle the UTF8 -> ASCII issues
                    # uline = line.decode("utf-8")
                    # line = uline.encode("ascii", "ignore")

                    line = line.strip().lower()
                    words = line.split(" ")
                    for word in words:

                        # Throw away single letters, for now
                        if len(word) < self.HP_MIN_LENGTH and word.isdigit() == False:
                            continue

                        # Create a new entry if you've never seen this word before
                        if word not in homophones:
                            homophones[word] = []

                        # For an entry of write/right
                        # homophones[word] = f7(homophones[word] + [w for w in words if w != word and len(w) >= HP_MIN_LENGTH])
                        homophones[word] = self.f7(
                            homophones[word] + [w for w in words if w != word])

                f.close()
        self.homophones = homophones

    # Return the main part of the domain
    # Drops TLDs and drops subdomains
    def cleanup_domain(self, domain):
        nr_dots = domain.count(".")
        parts = domain.split(".")

        if nr_dots == 1:
            return [parts[0], parts[1]]

        # Domains like: .co.uk, .co.in, and so on
        if parts[-2] in ["co", "com", "url", "net", "org", "gov", "ac", "edu", "me", "gob", "gen"]:
            return [parts[-3], '.'.join(parts[-2:])]

        # Check pairs
        pairs = [
            '.go.jp',
            '.ne.jp',
            '.gr.jp',
            '.or.jp',
            '.co.uk',
            '.sh.cn',
            '.cq.cn',
            '.nic.in',
            '.co.kr',
            '.or.kr',
            '.ne.kr',
            '.tx.us',
            '.nj.us',
            '.fl.us',
            '.ny.us',
            '.ca.us',
            '.pa.us',
            '.ga.us',
            '.qa.ca',
            '.qc.ca',
            '.on.ca',
            '.mus.br',
            '.jus.br',
            '.msk.ru'
        ]
        for p in pairs:
            if domain.endswith(p):
                return [parts[-3], '.'.join(parts[-2:])]

        if parts[-1] in ['fr', 'com', 'net', 'gr', 'be', 'uk']:
            return [parts[-2], parts[-1]]

        else:
            print("Didn't parse: %s " % domain)

        return [parts[-3], '.'.join(parts[-2:])]

    # Crazy expensive but works like a charm
    def remove_unintended_words(self, candidates, domain):

        start_time = time.time()
        cnt = 0

        # google.com -> google
        # files.wordpress.com -> wordpress
        # myfiles.co.uk -> myfiles
        original_domain = domain

        domain_length = len(domain)
        min_len_cand = len(min(candidates, key=len))

        # Reserved for really problematic domains
        blacklist = ['theamazingios6maps.tumblr.com', 'taboolasyndication.com']
        if original_domain in blacklist:
            return (False, candidates)

        # If we don't have enough words, there is no point in trying
        if len(''.join(candidates)) < domain_length:
            return (False, candidates)

        print("REMOVE Candidates: %s" % candidates)
        for c in self.all_combinations(candidates):
            # Return if we are over the limit of our string
            if (len(c) * min_len_cand) > domain_length:
                print("Over limit...")
                return (False, candidates)

            # Check the time limit... If it's taking too long, just return
            cnt += 1
            if (cnt % 5000) == 0:
                c_time = time.time()
                if (c_time - start_time) > self.MAX_TRY_SECS:
                    print("Timeout on slow method")
                    return (False, candidates)

            c_attempt = ''.join(c)

            if len(c_attempt) != domain_length:
                continue

            # We have found it, but it may not be the only one
            # TODO: find a fast way, if necessary
            if c_attempt == domain:
                return (True, list(c))

        return (False, candidates)

    # The purpose of this function is to remove unintended words
    # that exist in the middle of intended ones
    # e.g. leaseweb.com should be [lease,web] and not [lease,web,sew]
    def remove_unintended_words_fast(self, candidates, domain, tries=0, tried=[]):

        # Find the first word#############
        if tries == 0:

            first_word_matches = [c for c in candidates if domain.find(c) == 0]
            if len(first_word_matches) == 0:
                return candidates

            first_word = max(first_word_matches, key=len)

            new_order = []
            new_order.append(first_word)

            for c in candidates:
                if c not in first_word_matches:
                    new_order.append(c)

            candidates = new_order
        ################################

        domain_dot_i = domain.rfind('.')

        for w1 in candidates:
            multiple = [w1]
            for w2 in candidates:
                if w1 == w2:
                    continue

                # w1 = 'domain', w2 = 'lease', w1 + w2 = 'domainlease'
                constructed_word = w1 + w2
                if constructed_word == domain[:domain_dot_i]:
                    return [w1, w2]

                multiple.append(w2)

                if ''.join(multiple) == domain[:domain_dot_i]:
                    return multiple

        # Lets use chance :)
        if tries < 50:
            to_shuffle = candidates[1:]
            tried.append(''.join(to_shuffle))

            random.shuffle(to_shuffle)
            c_shuffles = 0

            # Re-shuffle if we've seen it before (Limited to a number, so that we don't infinite loop)
            while (''.join(to_shuffle) in tried):
                random.shuffle(to_shuffle)
                c_shuffles += 1
                if c_shuffles >= 20:
                    return candidates

            candidates[1:] = to_shuffle

            return self.remove_unintended_words_fast(candidates, domain, tries + 1, tried)
        else:
            # Return the same if we did not find anything
            return candidates

    def find_h_domains_single(self, domain):

        print("%s" % domain)
        sys.stdout.flush()

        # Used later on
        replace_helper = {}

        # If the domain contains slashes, we can break at these
        if "-" in domain:
            parts = domain.split(".")
            for p in parts:
                if "-" in p:
                    candidate_words = p.split("-")
                    break
        else:
            # Find if there are any dictionary words that are included in the domain
            domain_wo_tld = domain[:domain.rfind('.')]
            candidate_words = [w for w in self.wordlist if w in domain_wo_tld]
            candidate_words_original = candidate_words[:]
            # whitelist = ['ads','sex']

            print("Candidate words: %s" % candidate_words)

            # Remove words that are contained in others
            # e.g. if "use" and "user" are both found in the same domain, drop the use, keep the user

            # Problematic usecase: adultadworld.com #TODO: See how big this problem is
            delete_words = []
            for word_i in candidate_words:
                for word_j in candidate_words:
                    if word_i != word_j and word_i in word_j:  # and word_i not in whitelist:
                        word_j_index = domain.find(word_j)
                        word_i_index = domain.find(word_i)

                        crippled_domain = domain.replace(
                            word_j, ''.join('$' for x in range(len(word_j))))

                        if word_i not in crippled_domain:
                            delete_words.append(word_i)
                        else:
                            replace_helper[word_i] = crippled_domain.find(
                                word_i)

            for w in self.f7(delete_words):
                candidate_words.remove(w)

            print("Before: %s" % candidate_words)
            sys.stdout.flush()
            # Clean up the candidates
            if len(candidate_words) > 2:
                candidate_words = self.remove_unintended_words_fast(
                    candidate_words, domain)

                # If it didn't work out, use the other method
                if ''.join(candidate_words) != domain_wo_tld or '.'.join(candidate_words) != domain_wo_tld:
                    print("called slow version")
                    (has_succeeded, n_candidate_words) = self.remove_unintended_words(
                        candidate_words_original, domain)

                    if has_succeeded == True:
                        candidate_words = n_candidate_words

            print("After: %s" % candidate_words)

        print("Candidates: %s" % candidate_words)
        candidates = [
            homophone for homophone in self.homophones if homophone in candidate_words]

        s_domains = []

        for c in candidates:
            for h in self.homophones[c]:
                # Make one more check to ensure that the homophone is not in the TLD
                if domain.rfind(c) > domain.rfind("."):
                    continue

                if c not in replace_helper:
                    s_domain = domain.replace(c, h)
                else:
                    s_domain = domain[:replace_helper[c]] + \
                        h + domain[replace_helper[c] + len(c):]

                s_domains.append((s_domain, c))

                print("\tSSD: %s [%s -> %s] %s " % (domain, c, h, s_domain))

        # # Check if we can have more!
        double_s_domains = []
        if len(s_domains) > 1 and len(candidates) > 1:
            for (s_dom, old_c) in s_domains:
                for c in candidates:
                    if c in s_dom and c != old_c:
                        for h in self.homophones[c]:

                            if domain.rfind(c) > domain.rfind("."):
                                continue

                            double_s_domain = s_dom.replace(c, h)
                            if double_s_domain in double_s_domains or double_s_domain == domain:
                                continue
                            else:
                                double_s_domains.append(double_s_domain)

                            print("\tSSD: %s -> %s [%s -> %s] %s " %
                                (domain, s_dom, c, h, double_s_domain))

        print("")

        return {
            "domain_name": domain,
            "candidate_words": candidate_words,
            "soudsquatting_single": s_domains,
            "soudsquatting_double": double_s_domains,
        }

    def find_h_domains(self, domain_f, skip=0, limit=0):

        cnt = 0
        analyzed_domains = set([])

        for domain in domain_f:

            domain = domain.strip().split("/")[0]

            # Skip entries that are IP addresses
            try:
                socket.inet_aton(domain)
                continue
            except socket.error:
                pass

            # Lets focus only on PS+1 domains
            domain = '.'.join(self.cleanup_domain(domain))

            print(self.find_h_domains_single(domain))

            if skip > 0:
                skip -= 1
                continue

            # Handle the crappiness of Alexa lists.. some domains are existing domains with paths, e.g. feedproxy.google.com/~r
            # Also, since we drop the subdomains, only analyze the master domain once
            if domain in analyzed_domains:
                continue
            else:
                analyzed_domains.add(domain)

            # Optionally limit the number of domains searched
            cnt += 1
            if limit != 0 and cnt >= limit:
                break

    def get_homophones_length(self):
        print(self.homophones)
        return len(self.homophones.keys())
