#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  change hosts
#  Usage
#  sudo ./host.py dev
#
__author__ = 'xilei'

import sys
import os

hosts_dir = "./hosts"
prefix = "company-"
mode_tpl = "tpl"
host_path = "/etc/hosts"

tpl_repl = "{tpl}"

def usage():
	help_text = "usage: %s mode,all modes follow:\n\t%s " % (os.path.basename(__file__),"\n\t".join(get_all_modes()))
	print(help_text)
 
def get_mode_file(mode):
	"""
	get filename by mode and prefix
	"""
	if not mode:
		return False
	filename = os.path.abspath(hosts_dir+'/'+prefix+mode)
	if not os.path.exists(filename):
		return False
	else:
		return filename

def get_all_modes():
	modes = set()
	for name in os.listdir(hosts_dir):
		if not name.startswith(prefix):
			continue
		ninfo = name.split('-',maxsplit=1)
		if len(ninfo)<2:
			continue
		if ninfo[1] == mode_tpl:
			continue
		modes.add(ninfo[1])
	return modes

def get_current_mode():
	current_mode = ''
	with open(host_path,'r') as f:
		current_mode = f.readline().strip('#\n')
	return current_mode

def main(mode):	
	m_file = get_mode_file(mode)
	if not m_file:
		print("can not  find mode: %s"  % mode)
		return False
	print("change mode to %s" % mode)
	tpl_content = tpl_repl
	tpl_file = get_mode_file(mode_tpl)
	content = "#%s\n" % mode
	if tpl_file:
		with open(tpl_file,'r') as tf:
			tpl_content = tf.read()
	with open(m_file,'r') as mf:
		content += tpl_content.replace(tpl_repl,mf.read())		
	with open(host_path,'wb') as hf:
		hf.write(content.encode('utf-8'))
	print ("done.")
	return True

def check_permission(filename):
	try:
		with open(filename,"wb") as hf:
			pass
	except Exception as e :
		print(e)
		sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv)<2:		
		usage()
		print("current mode : %s" % get_current_mode())
		sys.exit(0)
	mode = sys.argv[1]
	check_permission(host_path)
	main(mode)
