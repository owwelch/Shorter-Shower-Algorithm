#!/bin/bash

for n in {1..10}; do
	for s in Start End; do
		sbatch << EOT
#!/bin/bash

#SBATCH --job-name="owelch_script"
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=8192
#SBATCH -o "/home/students/owelch/Shorter-Shower-Algorithm/results/2^"${n-1}"_neurons_"$s".csv"
#SBATCH -e "/home/students/owelch/Shorter-Shower-Algorithm/results/2^"${n-1}"_neurons_"$s".err"

cd /home/students/owelch/Shorter-Shower-Algorithm
python model.py $s $n

exit 0
EOT
	done
done
