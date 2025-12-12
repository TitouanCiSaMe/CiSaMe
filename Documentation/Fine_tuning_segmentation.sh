#! /bin/sh

#SBATCH -p publicgpu          # Partition GPU publique
#SBATCH -N 1                  # 1 nœud
#SBATCH -t 4:00:00            # Temps maximum : 4 heures
#SBATCH --gres=gpu:1          # 1 GPU
#SBATCH --constraint=gputc    # GPU tensor core
#SBATCH --mail-type=END       # Email à la fin
#SBATCH --mail-user=votre.email@unistra.fr

module load kraken
ketos segtrain --optimizer Adam --augment --workers 64 -d cuda:0 -f page --min-epochs 60 -w 0 --quit dumb 20 -N 2000 --resize new -i Model_de_base/NOM_MODELE_BASE.mlmodel -o Repertoire_model_finetune/NOM_PROJET/NOM_PROJET -s '[1,1200,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32]' -r 0.0001 Ground_Truth/NOM_PROJET/*.xml
