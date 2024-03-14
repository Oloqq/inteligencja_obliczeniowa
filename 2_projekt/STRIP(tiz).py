from strips import Problem, Action

# Definicja działań
move = Action('move(x,y,z)',
              precond='clear(y) & on(x,y) & clear(z)',
              effect='¬on(x,y) & ¬clear(z) & on(x,z) & clear(y)')

# Tworzenie problemu
problem1 = Problem(
    domain=[move],
    initial='on(a,b) & on(b,c) & ... & clear(a) & clear(y)',
    goals='on(a,y) & on(b,a) & ...'
)
