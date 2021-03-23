import tldextract
import sys
import os

package_directory = os.path.dirname(os.path.abspath(__file__))


class ts_models:
    f_fingers = {}

    def __init__(self):
        # Read in the qwerty maps
        f = open(os.path.join(package_directory, "qwerty.map"))
        for line in f:
            line = line.strip()
            parts = line.split(" ")
            self.f_fingers[parts[0]] = parts[1]
        f.close()

    def generate_ts_domains(self, fullDomain):
        ts_domains = {}

        # google.com -> ['google', '.com']
        # cl_domain = self.cleanup_domain(domain)
        fullDomain = fullDomain.lower()
        parts = tldextract.extract(fullDomain)
        cl_domain = [parts.domain, '.' + parts.suffix]
        f_clean_domain = ''.join(cl_domain)

        ts_domains[f_clean_domain] = {}

        cld_len = len(cl_domain[0])

        # Model 1: Character substitution, fat finger one
        ts_domains[f_clean_domain]["c_subs"] = []
        for i in range(0, cld_len):
            ts_characters = self.f_fingers[cl_domain[0][i]]
            for c in ts_characters:
                ts_domains[f_clean_domain]["c_subs"].append(
                    "%s%c%s%s" % (cl_domain[0][0:i], c, cl_domain[0][i + 1:], cl_domain[1]))

        # Model 2: Missing dot typos:
        # ts_domains[f_clean_domain]["c_mdot"] = []
        # nr_dots = f_clean_domain.count(".")
        #
        # ts_domains[f_clean_domain]["c_mdot"].append('www' + f_clean_domain)
        # if nr_dots == 2:
        #     dot_index = f_clean_domain.find(".")
        #     ts_domains[f_clean_domain]["c_mdot"].append(f_clean_domain[:dot_index] + f_clean_domain[dot_index + 1:])

        # Model 3: Character omission
        ts_domains[f_clean_domain]["c_omm"] = []
        for i in range(0, cld_len):
            ts_domains[f_clean_domain]["c_omm"].append(f_clean_domain[:i] + f_clean_domain[i + 1:])

        # Model 4: Character permutation
        ts_domains[f_clean_domain]["c_perm"] = []
        for i in range(0, cld_len - 1):
            if f_clean_domain[i + 1] != f_clean_domain[i]:
                ts_domains[f_clean_domain]["c_perm"].append(
                    f_clean_domain[:i] + f_clean_domain[i + 1] + f_clean_domain[i] + f_clean_domain[i + 2:])

        # Model 5: Character duplication
        ts_domains[f_clean_domain]["c_dupl"] = []
        for i in range(0, cld_len):
            ts_domains[f_clean_domain]["c_dupl"].append(
                f_clean_domain[:i] + f_clean_domain[i] + f_clean_domain[i] + f_clean_domain[i + 1:])

        return ts_domains[f_clean_domain]

    def generate_ts_tld(self, tld):
        ts_domains = []

        # google.com -> ['google', '.com']
        # cl_domain = self.cleanup_domain(domain)

        tld = tld.lower()
        tld = tldextract.extract(tld).suffix
        cl_domain = [tld, '']
        f_clean_domain = ''.join(cl_domain)

        cld_len = len(cl_domain[0])

        # Model 1: Character substitution, fat finger one
        for i in range(0, cld_len):
            ts_characters = self.f_fingers[cl_domain[0][i]]
            for c in ts_characters:
                newname = "%s%c%s%s" % (cl_domain[0][0:i], c, cl_domain[0][i + 1:], cl_domain[1])
                if tldextract.extract(newname).suffix != "":
                    ts_domains.append(newname)

        # Model 3: Character omission
        for i in range(0, cld_len):
            newname = f_clean_domain[:i] + f_clean_domain[i + 1:]
            if tldextract.extract(newname).suffix != "":
                ts_domains.append(newname)

        # Model 4: Character permutation
        for i in range(0, cld_len - 1):
            if f_clean_domain[i + 1] != f_clean_domain[i]:
                newname = f_clean_domain[:i] + f_clean_domain[i + 1] + f_clean_domain[i] + f_clean_domain[i + 2:]
                if tldextract.extract(newname).suffix != "":
                    ts_domains.append(newname)

        # Model 5: Character duplication
        for i in range(0, cld_len):
            newname = f_clean_domain[:i] + f_clean_domain[i] + f_clean_domain[i] + f_clean_domain[i + 1:]
            if tldextract.extract(newname).suffix != "":
                ts_domains.append(newname)

        return ts_domains


def usage():
    print("Usage:")
    print("ts_models.py <domain name>")
    print("")
    print("example:")
    print("ts_models.py www.google.com")
    print("")
