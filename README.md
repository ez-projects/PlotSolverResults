"""
Plot graph for thesis using matlibplot
"""

Quick setup — if you've done this kind of thing before

https://github.com/zhouen/GitConfig.git

We recommend every repository include a README, LICENSE, and .gitignore.
…or create a new repository on the command line

echo "# GitConfig" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/zhouen/GitConfig.git
git push -u origin master

…or push an existing repository from the command line

git remote add origin https://github.com/zhouen/GitConfig.git
git push -u origin master
========================================================================================================================

plot_timesteps_line.py
    - plot timesteps vs time (h) of each solver across all mesh sizes

plot_matrix.py
    - plot a given matrix structure, size larger than 20k will raise a memory error

plot_total_time.py
    - plot total solve and analysis time with line