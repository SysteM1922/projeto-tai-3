#include <iostream>
#include <string>
#include <getopt.h>
#include <fstream>
#include <filesystem>
#include <map>

using namespace std;
namespace fs = std::filesystem;

string temp_folder = "temp";
string extension = "";

int compress_and_get_size(string compressor, string file);
string concat_signatures(string compressor, string file1, string file2);
float ncd(int x_size, int y_size, int xy_size);
void set_extension(string compressor);
string get_file_name(string file);

int main(int argc, char* argv[]) {

    string compressor = "gzip";
    string sample = "";
    string freqs_folder = "";

    if (argc < 5) {
        cerr << "Usage: find_music [ -c compressor ] [ -s sample ] [ -f freqs_folder ]" << endl;
        return 1;
    }

    int opt;
    while ((opt = getopt(argc, argv, "c:s:f:")) != -1) {
        switch (opt) {
            // compressors: gzip, bzip2, lzma, zstd, xz, lzop, lz4
            case 'c':
                if (string(optarg) != "gzip" && string(optarg) != "bzip2" && string(optarg) != "lzma" && string(optarg) != "zstd" && string(optarg) != "xz" && string(optarg) != "lzop" && string(optarg) != "lz4") {
                    cerr << "Error: invalid compressor" << endl;
                    return 1;
                }
                compressor = optarg;
                break;
            case 's':
                sample = optarg;
                break;
            case 'f':
                freqs_folder = optarg;
                break;
            default:
                cerr << "Usage: find_music [ -c compressor ] [ -s sample ] [ -f freqs_folder ]" << endl;
                return 1;
        }
    }

    // Check if the compressor is available
    if (system(("which " + compressor + " > /dev/null").c_str()) != 0) {
        cerr << "Error: " << compressor << " is not available" << endl;
        return 1;
    }

    set_extension(compressor);

    string extra_args = "";
    // read args from freqs_folder args file
    ifstream args_file(freqs_folder + "/args");
    if (args_file.is_open()) {
        string line;
        while (getline(args_file, line)) {
            extra_args = line;
        }
        args_file.close();
    }

    if (!fs::exists(temp_folder)) {
        fs::create_directory(temp_folder);
    }

    // get the signature of the sample
    string command = "./GetMaxFreqs/bin/GetMaxFreqs -w \"" + temp_folder + "/sample.freqs\"" + extra_args + " '" + sample + "'";
    if (system(command.c_str()) != 0) {
        cerr << "Error: could not generate the signature of the sample" << endl;
        return 1;
    }

    // compress the signature and get the size of the compressed file
    int sample_size = compress_and_get_size(compressor, temp_folder + "/sample.freqs");

    map<float, string> music_ncd;

    string music_signature_path = "";
    string music_name = "";
    int music_signature_size = 0;
    string concat_file = "";
    int concat_size = 0;
    for (const auto & entry : fs::directory_iterator(freqs_folder)) {
        if (entry.path().extension() != ".freq") {
            continue;
        }
        music_signature_path = entry.path();
        music_signature_size = compress_and_get_size(compressor, music_signature_path);
        if (music_signature_size == -1) {
            cerr << "Error: could not compress the signature of the music" << endl;
            return 1;
        }

        concat_file = concat_signatures(compressor, temp_folder + "/sample.freqs", music_signature_path);
        if (concat_file == "") {
            cerr << "Error: could not concatenate the signature of the sample and the music" << endl;
            return 1;
        }
        concat_size = compress_and_get_size(compressor, concat_file);
        if (concat_size == -1) {
            cerr << "Error: could not compress the concatenated signature of the sample and the music" << endl;
            return 1;
        }

        music_name = get_file_name(music_signature_path);
        music_ncd[ncd(sample_size, music_signature_size, concat_size)] = music_name;
    }

    for (auto it = music_ncd.rbegin(); it != music_ncd.rend(); ++it) {
        cout << it->first << " : " << it->second << endl;
    }

    fs::remove_all(temp_folder);

    return 0;
}

int compress_and_get_size(string compressor, string file) {
    string file_name = get_file_name(file);
    string command = compressor + " -c \'" + file + "\' > \'" + temp_folder + "/" + file_name + "." + extension + "\'";
    if (system(command.c_str()) != 0) {
        return -1;
    }

    ifstream sample_file(temp_folder + "/" + file_name + "." + extension);
    if (!sample_file.is_open()) {
        return -1;
    }

    sample_file.seekg(0, ios::end);
    int sample_size = sample_file.tellg();
    sample_file.close();

    return sample_size;
}

string concat_signatures(string compressor, string file1, string file2) {
    string file1_name = get_file_name(file1);
    string file2_name = get_file_name(file2);

    string command = "cat \'" + file1 + "\' \'" + file2 + "\' | " + compressor + " > \'" + temp_folder + "/" + file1_name + "_" + file2_name + ".freq" + "\'";
    if (system(command.c_str()) != 0) {
        return "";
    }

    return temp_folder + "/" + file1_name + "_" + file2_name + ".freq";
}

float ncd(int x_size, int y_size, int xy_size) {
    return (float)(xy_size - min(x_size, y_size)) / max(x_size, y_size);
}

void set_extension(string compressor) {
    if (compressor == "gzip") {
        extension = "gz";
    } else if (compressor == "bzip2") {
        extension = "bz2";
    } else if (compressor == "lzma") {
        extension = "lzma";
    } else if (compressor == "zstd") {
        extension = "zst";
    } else if (compressor == "xz") {
        extension = "xz";
    } else if (compressor == "lzop") {
        extension = "lzo";
    } else if (compressor == "lz4") {
        extension = "lz4";
    }
}

string get_file_name(string file) {
    string file_name = file.substr(file.find_last_of("/\\") + 1);
    return file_name.substr(0, file_name.find_last_of("."));
}