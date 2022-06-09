
#include <direct.h>
#include <filesystem>
#include <filesystem>

using namespace std;




int main(int argc, char * argv[]) {
		
		
	if(argc<2) {
		program_statement(argv[0]);
		return -1;
	}

	
	if(paras._set_(argc, argv)==false)
		return -1;

	paras.print();
	
	string netfile=paras.file1;
	
	
	{	/* check if file_name exists */
		char (*b) = new char[netfile.size()+1];
		cast_string_to_char(netfile, b);
		ifstream inb(b);
		if(inb.is_open()==false) {
			
			cout<<"File "<<netfile<<" not found"<<endl;
			return false;
		
		}	
		delete[] b;
	}	/* check if file_name exists */

	
	oslom_net_global luca(netfile);
	
	
	
	
	
	if(luca.size()==0 || luca.stubs()==0) {
		cerr<<"network empty"<<endl;
		return -1;
	}
	
	
	
	LOG_TABLE._set_(cast_int(luca.stubs()));
	
	
	
	char directory_char[1000];
	cast_string_to_char(paras.file1, directory_char);
	char char_to_use[1000];
	//sprintf(char_to_use, "mkdir %s_oslo_files", directory_char);
	string dir_to_make;
	dir_to_make = std::string(directory_char) + "_oslo_files";
	//std::filesystem::remove_all(dir_to_make.c_str());
	_mkdir(dir_to_make.c_str());
	int sy=system(char_to_use);
	//sprintf(char_to_use, "rm -r %s_oslo_files/*", directory_char);
	//sy=system(char_to_use);
	
	
	cout<<"output files will be written in directory: "<<directory_char<<"_oslo_files"<<endl;
	
	//luca.draw_with_weight_probability("prob");
	oslom_level(luca, directory_char);
	
	
	return 0;
	
	

}


