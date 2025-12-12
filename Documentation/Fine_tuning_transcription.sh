#! /bin/sh

#SBATCH -p publicgpu   # 'p' pour Partition (file d'attente) public avec des GPU
#SBATCH -N 1          # 1 nœud, kraken utilisera dans tous les cas 1 seul noeud. 
#SBATCH -t 4:00:00           # Le job sera tué au bout de 4h
#SBATCH --gres=gpu:1   # Il y a 4 GPU par nœud, Kraken n’en nécessite qu’un seul
#SBATCH --constraint=gputc    # Nœuds GPU double précision, nous on va prendre gpu tensor core = puce spécialisé dans le deeplearning
#SBATCH --mail-type=END       # Réception d'un mail à la fin du job
#SBATCH --mail-user=votre.email@unistra.fr

module load kraken
ketos compile --random-split 0.8 0.1 0.1 --workers 64 -f xml -o DOSSIER_DE_SORTIE/NOM.arrow GT_CHEMIN/*.xml
ketos -v train --optimizer Adam --augment --workers 64 -d cuda:0 --min-epochs 20 -w 0 --quit dumb --pad 24 -w 0 -o Repertoire_model_finetune/NOM_PROJET/NOM_PROJET -s '[1,128,0,1 Cr4,16,32 Do0.1,2 Mp2,2 Cr4,16,32 Do0.1,2 Mp2,2 Cr3,8,64 Do0.1,2 Mp2,2 Cr3,8,64 Do0.1,2 S1(1x0)1,3 Lbx256 Do0.3,2 Lbx256 Do0.3,2 Lbx256 Do0.3]' -f binary -r 0.0001 --resize new -i Model_de_base/NOM_MODELE_BASE.mlmodel GT_compile/NOM.arrow
