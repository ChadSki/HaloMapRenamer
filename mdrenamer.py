#!/usr/bin/env python

# Copyright (c) 2014, Null <foo.null@yahoo.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import struct

def parseArguments(arguments):
	inputPath = arguments[0]
	modName = arguments[1]
	shortName = arguments[2]
	buildNumberString = arguments[3]
	outputDirectory = arguments[4] if len(arguments) >= 5 else os.path.dirname(inputPath)

	if not os.path.exists(inputPath):
		raise Exception("%s does not exist" % inputPath)

	if not inputPath.endswith(".map"):
		raise Exception("%s is not a .map file" % inputPath)

	if os.path.isdir(inputPath):
		raise Exception("%s is a directory.. which is not good" % inputPath)

	try:
		buildNumber = int(buildNumberString)
	except ValueError:
		raise Exception("Build number is not a valid number")

	if buildNumber <= 0:
		raise Exception("Build number is too small")

	if len(shortName) == 0:
		raise Exception("Short name cannot be empty")

	if len(modName) > 13:
		raise Exception("Mod name must be less than 13 characters")

	if len(modName) == 0:
		raise Exception("Mod name must be greater than 0 characters")

	mapFileName = "%s_%d" % (shortName, buildNumber)
	if len(mapFileName) > 13:
		raise Exception("Map name is too long. Try shortening the short name")

	if mapFileName.lower() != mapFileName:
		raise Exception("Map name has capital letter. The short name must be all lowercase")

	outputPath = os.path.join(outputDirectory, mapFileName + ".map")
	if os.path.exists(outputPath):
		raise Exception("Map already exists at %s ..aborting for safety.." % outputPath)

	return inputPath, outputPath, mapFileName, modName

def mdRenameFile(arguments):
	inputPath, outputPath, mapFileName, modName = parseArguments(arguments)
	with open(inputPath, "rb") as inputFile:
		mapBuffer = bytearray(inputFile.read())

	readBytes = lambda offset, length: mapBuffer[offset:offset + length]
	readUInt32Little = lambda offset: struct.unpack('<I', readBytes(offset, 0x4))[0]
	hasBytes = lambda offset, bytes: mapBuffer[offset:offset + len(bytes)] == bytes
	def writeBytes(offset, bytes, zeroPaddingLength=0):
		mapBuffer[offset:offset + zeroPaddingLength] = b"\x00" * zeroPaddingLength
		mapBuffer[offset:offset + len(bytes)] = bytes

	if readUInt32Little(0x4) != 7:
		raise Exception("This is not a valid (version 7) full-version map!")

	writeBytes(0x20, mapFileName.encode("utf-8"), 0xF)

	indexOffset = readUInt32Little(0x10)
	magic = readUInt32Little(indexOffset) - indexOffset - 0x28
	numberOfTags = readUInt32Little(indexOffset + 0xC)
	tagArrayOffset = indexOffset + 0x28

	for tagIndex in range(numberOfTags):
		currentLocation = 0x20 * tagIndex + tagArrayOffset
		if readBytes(currentLocation, 0x4) != b"rtsu":
			continue

		tagOffset = readUInt32Little(currentLocation + 0x10) - magic

		if hasBytes(tagOffset, b"ui\\shell\\main_menu\\mp_map_list"):
			namesOffset = readUInt32Little(currentLocation + 0x14) - magic + 0x1B0

			writeBytes(namesOffset + 0x48, "Random".encode("utf-16le"), (len("Rat Race") + 1) * 2)
			writeBytes(namesOffset + 0xB4, "Barrier".encode("utf-16le"), (len("Boarding Action") + 1) * 2)
			writeBytes(namesOffset + 0xD4, "Blood Gulch".encode("utf-16le"), (len("Blood Gulch") + 1) * 2)
			writeBytes(namesOffset + 0x174, "Crossing".encode("utf-16le"), (len("Infinity") + 1) * 2)
			writeBytes(namesOffset + 0x1A0, modName.encode("utf-16le"), (len("Gephyrophobia") + 1) * 2)

		elif hasBytes(tagOffset, b"ui\\shell\\main_menu\\multiplayer_type_select\\mp_map_select\\map_data"):
			descriptionOffset = readUInt32Little(currentLocation + 0x14) - magic + 0x19C
			originalBloodgulchBytes = bytes([0x54, 0x00, 0x68, 0x00, 0x65, 0x00, 0x20, 0x00, 0x51, 0x00, 0x75, 0x00, 0x69, 0x00, 0x63, 0x00, 0x6B, 0x00, 0x20, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x61, 0x00, 0x6E, 0x00, 0x64, 0x00, 0x20, 0x00, 0x74, 0x00, 0x68, 0x00, 0x65, 0x00, 0x20, 0x00, 0x44, 0x00, 0x65, 0x00, 0x61, 0x00, 0x64, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x34, 0x00, 0x2D, 0x00, 0x31, 0x00, 0x36, 0x00, 0x20, 0x00, 0x70, 0x00, 0x6C, 0x00, 0x61, 0x00, 0x79, 0x00, 0x65, 0x00, 0x72, 0x00, 0x73, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x53, 0x00, 0x75, 0x00, 0x70, 0x00, 0x70, 0x00, 0x6F, 0x00, 0x72, 0x00, 0x74, 0x00, 0x73, 0x00, 0x20, 0x00, 0x76, 0x00, 0x65, 0x00, 0x68, 0x00, 0x69, 0x00, 0x63, 0x00, 0x6C, 0x00, 0x65, 0x00, 0x73, 0x00])

			writeBytes(descriptionOffset + 0x12C, "Where would you\r\nlike to go?".encode("utf-16le"), 0x56)
			writeBytes(descriptionOffset + 0x2BC, "So Close,\r\nYet So Far..".encode("utf-16le"), 0x48)
			writeBytes(descriptionOffset + 0x308, originalBloodgulchBytes)
			writeBytes(descriptionOffset + 0x634, "A Memorial to\r\nHeroes Fallen".encode("utf-16le"), 0x86)
			writeBytes(descriptionOffset + 0x740, "Modded".encode("utf-16le"), 0x64)

	with open(outputPath, "wb") as outputFile:
		outputFile.write(mapBuffer)

	return outputPath

if __name__ == '__main__':
	if len(sys.argv[1:]) == 0:
		print("Usage: %s <input_map> <mod_name> <short_name> <build_number> [output_directory]\n" % sys.argv[0])
		print("Example: %s ~/Desktop/Maps/bloodgulch.map \"Best Mod\" bestmod 1\n" % sys.argv[0])
		print("Arguments:\n")
		print("<input_map> The file path to the Halo map file to rename\n")
		print("<mod_name> The user friendly name of the mod. Must be <= 13 characters; truncate if necessary. This is not the same as the name that shows up in the MD database, but the one that shows in the map selection menu in-game.\n")
		print("<short_name> The internal name of the mod that will be used in the outputting filename. Must be all lowercase and >= 1 character(s)\n")
		print("<build_number> The build number of the mod which is also used in the outputting filename. This should be increased before any sort of public or private distribution. Must be an integer >= 1\n")
		print("[output_directory] The directory to output the new MD renamed map in. This is optional and defaults to the directory <input_map> is in\n")
		print("Additionally, the following constraint must be met:")
		print("string_length(<short_name>) + string_length(<build_number>) < 13")
	else:
		mdRenameFile(sys.argv[1:])