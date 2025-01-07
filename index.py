from votes import Votes

name = 'bbbbb';
votes = {
    "1": 'c',
    "3": 'a',
    "2": 'd'
}

new_votes = Votes()

# new_votes.insert(name, votes)
#
# print(new_votes.show_all())
# new_votes.find_by_name("aaaa")
# new_votes.delete('677c10ab63661108740710bd')

print(new_votes.find_by_votes('d'))

# print(new_votes.edit("677d13627685800891dcb7f9", 'votes',votes ))