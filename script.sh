#!/bin/bash

for n in 0 1 2 3 4 5 6 7; do
	for s in Start End; do
		sbatch << EOT
#!/bin/bash

#SBATCH --job-name="owelch_script"
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=0
#SBATCH -o "/home/students/owelch/Shorter-Shower-Algorithm/results/2^"${n}"_neurons_"$s".csv"
#SBATCH -e "/home/students/owelch/Shorter-Shower-Algorithm/results/2^"${n}"_neurons_"$s".err"

cd /home/students/owelch/Shorter-Shower-Algorithm
python model.py $s $n

exit 0
EOT
	done
done
