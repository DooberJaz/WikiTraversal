
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Reader;
import java.util.Scanner;

public class WikiTrimmer {
	// Wiki pages will now be filtered to look like this:
	// >pagename
	// [Page links

	public static void main(String args[]) {
		Reader fileReader;
		Reader fileReader2;
		try {
			// This stores the links for each page that have already been used, preventing
			// duplicates
			ArrayList<String> repeats = new ArrayList<String>();
			// This creates a file containing all of the pages and associated links
			PrintWriter out = new PrintWriter(new FileWriter("WeightedWiki.txt"));
			// This takes in the original wikipedia file from local storage
			fileReader = new FileReader("WikipediaV2.txt");
			
			// This is here to remove the many broken links in wikipedia
			// Its likely that these links would work in wikipedia, however making them work here
			// Would be incredibly difficult and time consuming
			fileReader2 = new FileReader("BrokenLinks.txt");
			PrintWriter outBroken = new PrintWriter(new FileWriter("NewBrokenLinks.txt"));
			

			// wiki gets every page, remover shortens the pages
			Scanner wiki = new Scanner(fileReader);
			Scanner remover = null;
			Scanner cleanup = null;
			
			// This gets the list of broken links provided by later classes and makes sure 
			//those broken links aren't included
			// in future versions of the Wikipedia Document
			ArrayList<String> brokenLinks = new ArrayList<String>();
			cleanup = new Scanner(fileReader2);
			while (cleanup.hasNext()) {
				String noRepeats = cleanup.nextLine();
				if(!brokenLinks.contains(noRepeats)) {
					outBroken.write(noRepeats + "\n");
					brokenLinks.add(noRepeats);
				}
			}
			cleanup.close();
			outBroken.close();

			String temp;
			boolean afterLine;
			String temp2 = "";

			// this skips the initial general information in the document
			wiki.useDelimiter("<page>");
			wiki.next();

			while (wiki.hasNext()) {
				repeats.clear();
				remover = new Scanner(wiki.next());
				// This is complex but it allows the formatting defined above in quite an
				// efficient manner
				remover.useDelimiter("<title>");
				remover.next();
				remover.useDelimiter(">");
				remover.next();
				remover.useDelimiter("</title>");

				// lower case is used so there are no issues between pages
				temp = remover.next();
				if (temp.startsWith(">Template") || temp.startsWith(">Category") || temp.startsWith(">Wikipedia:", 0)
						|| temp.startsWith(">wikipedia:", 0) || temp.startsWith(">Module:", 0)) {

				} else {
					out.print(temp.toLowerCase() + "|2048");
					remover.useDelimiter("\\[\\[");
					remover.next();
					while (remover.hasNext()) {
						remover.useDelimiter("");
						remover.next();
						remover.next();
						remover.useDelimiter("\\]\\]");
						temp = remover.next();
						temp = temp.toLowerCase();

						// These are somewhat useless too the project, and therefore ignored
						// Some are downright stupid and I have no clue what some of the Wikipedia
						// contributors are doing
						if ((temp.startsWith("file:", 0)) || (temp.startsWith("d:", 0)) || (temp.startsWith("help:", 0))
								|| (temp.startsWith("user talk:", 0)) || (temp.startsWith("image:", 0))
								|| (temp.startsWith("id:", 0)) || (temp.startsWith("tr:", 0))
								|| (temp.startsWith(":file:", 0)) || (temp.startsWith("special:", 0))
								|| (temp.startsWith("wp:", 0)) || (temp.startsWith("wikt:", 0))
								|| (temp.startsWith(":wikt:", 0)) || (temp.startsWith("wikipedia:", 0))
								|| (temp.startsWith("category:", 0)) || (temp.startsWith(":", 0))
								|| (temp.startsWith("template:", 0)) || (temp.startsWith("category :", 0))
								|| (temp.startsWith("c:", 0)) || (temp.startsWith("m:", 0))
								|| (temp.startsWith("user:", 0)) || (temp.startsWith("commons:", 0))
								|| temp.startsWith("mediawiki:") || brokenLinks.contains(temp)
								|| temp.startsWith("project:") || temp.startsWith("cs:")) {
							remover.useDelimiter("\\[\\[");
							if (remover.hasNext()) {
								remover.next();
							}

						} else {
							// in wikipedia, some links are formatted "[linkname | actual text on page]
							// this code only needs the linkname, so ignores the rest
							if (temp.contains("|")) {
								afterLine = false;
								for (int i = 0; i < temp.length() - 1; i++) {
									if (afterLine == false) {
										if (temp.charAt(i) == '|') {
											afterLine = true;
										} else {
											temp2 = temp2 + temp.charAt(i);
										}
									}
								}
								temp = temp2;
								temp2 = "";
							}

							// Some links have a # in them to signify a certain part of a page (eg.
							// Birthday#Birthstone)
							// This will just assume like a player would, that the entire page is fair game
							if (temp.contains("#")) {
								// Some links start with a # for some godknows unforseen reason to me
								if (temp.startsWith("#")) {

								} else {
									afterLine = false;
									for (int i = 0; i < temp.length() - 1; i++) {
										if (afterLine == false) {
											if (temp.charAt(i) == '#') {
												afterLine = true;
											} else {
												temp2 = temp2 + temp.charAt(i);
											}
										}
									}
									temp = temp2;
									temp2 = "";
								}
							}

							if (temp.contains("/comment")) {
								cleanup = new Scanner(temp);
								cleanup.useDelimiter("/comment");
								if (cleanup.hasNext()) {
									temp = cleanup.next();
								} else {
									temp = "";
								}
								cleanup.close();
							} else if (temp.contains("{{")) {
								cleanup = new Scanner(temp);
								cleanup.useDelimiter("\\{\\{");
								if (cleanup.hasNext()) {
									temp = cleanup.next();
								} else {
									temp = "";
								}
								cleanup.close();
							}
							// this avoids repeating links
							if (!repeats.contains(temp) && temp != "") {
								out.print("[" + temp);
								repeats.add(temp);
							}
							remover.useDelimiter("\\[\\[");
							if (remover.hasNext()) {
								remover.next();
							}
						}
					}
				}
			}

			out.close();
			wiki.close();
			remover.close();
		} catch (FileNotFoundException e) {

		} catch (IOException e) {

		}
	}
}
