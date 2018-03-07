import os, sys, subprocess



repos = ["http://145.108.225.21/gitlab/t-yoshi_peca-android.git", "http://145.108.225.21/gitlab/ekylibre_zero-android.git", "http://145.108.225.21/gitlab/intari_readingtracker.git", "http://145.108.225.21/gitlab/rabid_nzsl-dictionary-android.git", "http://145.108.225.21/gitlab/yh1224_wifistate.git", "http://145.108.225.21/gitlab/nightlynexus_material-cards.git", "http://145.108.225.21/gitlab/croconaut_wifon.git", "http://145.108.225.21/gitlab/hishammuneer_blackjack_game.git", "http://145.108.225.21/gitlab/horaapps_leafpic.git", "http://145.108.225.21/gitlab/dpcsoftware_expenses.git", "http://145.108.225.21/gitlab/ixkor_callerinfo.git", "http://145.108.225.21/gitlab/vriesderick_roosterwijzigingchecker.git", "http://145.108.225.21/gitlab/androidfu_now-playing.git", "http://145.108.225.21/gitlab/xtensa_podemu.git", "http://145.108.225.21/gitlab/scoles2428_blabbermouth.git", "http://145.108.225.21/gitlab/wktk_meiji-wireless-login.git", "http://145.108.225.21/gitlab/alimehrpour_clipbox.git", "http://145.108.225.21/gitlab/globaltechnology_gma-android.git", "http://145.108.225.21/gitlab/ojacquemart_vlillechecker.git", "http://145.108.225.21/gitlab/bravelocation_yeltzland-android.git"]

for repo in repos:
	callString = "git clone " + repo
	subprocess.call(callString, shell=True)