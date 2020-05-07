import random
from collections import deque


class Page:
    # this is used for BFS
    def __init__(self, name, parent, weight):
        self.name = name
        self.parent = parent
        self.weight = weight


class Node:
    # this is used for dijkstra's, it needs a few more variables than BFS
    def __init__(self, name, parent, weight, size):
        self.name = name
        self.weight = weight
        self.size = size
        self.parent = parent


clicked_links = []


def initialise_wiki():
    wikiText = open("FullWeightedWiki.txt", "r").read()
    dictionary = {}
    read = wikiText.split(">")
    for page in read:
        head, *tail = page.split("[")
        if len(tail) > 0:
            head, weight = head.split("|")
            if head != tail[0]:
                # Some pages have multiple pages for them, however one of the pages has one link, which is the
                # page name with underscores instead of spaces. It really messes with things so this stops that
                if head != tail[0].replace("_", " "):
                    dictionary[head] = weight, tail
    print("Total Wikipedia pages: " + str(len(dictionary)))
    # The dictionary contains the weight of a page (used in some algorithms), and the available links to a page
    # for every page in Wikipedia
    return dictionary


def main():
    dictionary = initialise_wiki()
    # Default values
    start_page = "tree"
    final_target = "artificial intelligence"
    method = "random"
    success = False

    # User input for ease of use
    while not success:
        print("Input a start page, leave black to use default value")
        print("Input /random to generate and use a random page")
        page = input().lower()
        if page == "/random" or page == "/r":
            while not success:
                try:
                    start_page = random.choice(list(dictionary))
                    temp = dictionary[start_page]
                    success = True
                except KeyError:
                    success = False
        elif page != "":
            try:
                temp = dictionary[page]
                start_page = page
                success = True
            except KeyError:
                success = False
                print("\n\nThat page does not exist")
        else:
            success = True

    print("The start page is: " + start_page)
    success = False

    while not success:
        print("Input a target page, leave black to use default value")
        print("Input /random to generate and use a random page")
        page = input().lower()
        if page == "/random" or page == "/r":
            while not success:
                try:
                    final_target = random.choice(list(dictionary))
                    temp = dictionary[start_page]
                    success = True
                except KeyError:
                    success = False
        elif page != "":
            try:
                temp = dictionary[page]
                final_target = page
                success = True
            except KeyError:
                success = False
                print("\n\nThat page does not exist")
        else:
            success = True

    print("The target page is: " + final_target)

    num = 0
    while num < 1 or num > 4:
        print("Welcome")
        print("Enter 1 for random")
        print("Enter 2 for dijkstras")
        print("Enter 3 for BFS")
        print("Enter 4 to automatically assign weights")
        num = int(input())
        print("")
        print("")
    if num == 1:
        num = 0
        while num < 1 or num > 3:
            print("Enter 1 for pure random")
            print("Enter 2 for random with no repeated pages clicked")
            print("Enter 3 for random with a stack (it exhausts all links, almost like BFS)")
            num = int(input())
        if num == 1:
            method = "random"
        elif num == 2:
            method = "random_no_repeat"
        elif num == 3:
            method = "random_stack"
    elif num == 2:
        num = 0
        while num < 1 or num > 2:
            print("Enter 1 for dijkstra's alone")
            print("Enter 2 to apply weights for the final target and then run dijkstra's")
            num = int(input())
            if num == 1:
                method = "dijkstra"
            elif num == 2:
                method = "assign_weights_dijkstra"
    elif num == 3:
        num = 0
        while num < 1 or num > 6:
            print("Enter 1 for pure BFS")
            print("Enter 2 for BFS with no repeats")
            print("Enter 3 for BFS with some repeats")
            print("Enter 4 for weighted BFS (used by other algorithms)")
            print("Enter 5 for weighted BFS with no repeats")
            print("Enter 6 for weighted BFS with some repeats")
            num = int(input())
        if num == 1:
            method = "BFS"
        elif num == 2:
            method = "BFS_no_repeats"
        elif num == 3:
            method = "BFS_some_repeats"
        elif num == 4:
            method = "weighted_BFS"
        elif num == 5:
            method = "weighted_BFS_no_repeats"
        elif num == 6:
            method = "weighted_BFS_some_repeats"
    elif num == 4:
        method = "assign_weights"

    if (method == "random_stack") or (method == "random_no_repeat") or (method == "random"):
        # This is for methods that run through the graph without mapping it (they choose a path)
        traverse_wiki(dictionary, final_target, start_page, method)
    elif method.startswith("assign_weights"):
        if method == "assign_weights_dijkstra":
            dictionary = assign_weights2(dictionary, final_target, method)
            search_wiki(dictionary, final_target, start_page, method)
        else:
            assign_weights2(dictionary, final_target, method)
    else:
        # This is for methods that run through the graph in a more searching way (BFS, Djikstras, etc.)
        search_wiki(dictionary, final_target, start_page, method)


def traverse_wiki(dictionary, final_target, current_page, method):
    num_broken_links = 0
    broken_link_list = []
    weight, available_links = dictionary[current_page]
    num_clicks = 1
    global clicked_links
    next_page = ""

    while next_page != final_target:
        try:
            next_page = get_method(method, available_links)
            if next_page == "Unable to reach endpoint":
                print("Unable to reach endpoint")
                break

            print(next_page)
            weight, available_links = dictionary[next_page]
            num_clicks += 1
            clicked_links.append(current_page)
            current_page = next_page
        except KeyError:
            clicked_links.append(next_page)
            # Documentation of every broken link I encountered
            # This is inefficient code and ugly as hell, but i'm coding for my time efficiency as
            # at the final product stage this shouldn't be used much, if at all
            broken_link = open('BrokenLinks.txt', 'r')
            broken_link_list = [broken_link.readline().strip('\n')]
            while broken_link_list[len(broken_link_list) - 1] != "":
                broken_link_list.append(broken_link.readline().strip('\n'))
            broken_link.close()
            broken_link = open('BrokenLinks.txt', 'a')
            if next_page not in broken_link_list:
                print("Broken link found")
                broken_link.write(next_page + "\n")
                broken_link.close()
                num_broken_links += 1
            else:
                try:
                    clicked_links.pop()
                    available_links = dictionary[clicked_links.pop()]
                except KeyError:
                    print("Infinite Link Loop")
                    break

    if next_page != final_target:
        clicked_links.append(current_page)
        print("Done")

    print("Removed " + str(num_broken_links) + " broken links")
    print("Number of clicks: " + str(num_clicks))
    clicked_links.clear()
    broken_link_list.clear()


def get_method(method, available_links):
    global clicked_links
    # depending on method, gets the decision function for that
    if method == "random":
        link = available_links[random.randint(0, len(available_links) - 1)]
        return link
    elif method == "random_no_repeat":
        # This can sometimes break due to clicking a page with only one link, which
        # leads back to the page before it
        no_repeats_list = [i for i in available_links if i not in clicked_links]
        print(no_repeats_list)

        if len(no_repeats_list) == 0:
            return "Unable to reach endpoint"

        link = no_repeats_list[random.randint(0, len(no_repeats_list) - 1)]
        return link
    elif method == "random_stack":
        # random_stack functions the same as no repeat, but stores previously visited pages on a stack, it will
        # go back up the stack whenever there can be no more repeats. This means it should always eventually make it to
        # the destination, though it could take a LONG time
        return random_stack(available_links)


def random_stack(available_links):
    global clicked_links
    no_repeats_list = [i for i in available_links if i not in clicked_links]

    while len(no_repeats_list) == 0:
        clicked_links.pop()
        no_repeats_list = [i for i in available_links if i not in clicked_links]

    link = no_repeats_list[random.randint(0, len(no_repeats_list) - 1)]
    return link


def search_wiki(dictionary, final_target, start_page, method):
    global clicked_links

    if method.startswith("BFS"):
        bfs(dictionary, final_target, start_page, method)

    elif method.startswith("weighted_BFS"):
        # This runs BFS and adds/changes weights for the links, allowing for djikstras and A* algorithms later
        weighted_bfs(dictionary, final_target, start_page, method)

    elif method == "dijkstra" or method == "assign_weights_dijkstra":
        # This runs dijkstras on the weights gained from weighted BFS
        dijkstra(dictionary, final_target, start_page, method)


def bfs(dictionary, final_target, start_page, method):
    num_broken_links = 0
    broken_link_list = []
    next_page = ""
    future_queue = deque()
    past_queue = deque()
    # Weight set higher than any other to prevent returning back to the start
    start = Page(start_page, "no--parent", 0)
    future_queue.append(start)
    clicks_in_layer = 1
    clicks = 0
    total_pages = 0
    while len(future_queue) > 0:
        try:
            next_obj = future_queue.popleft()
            next_page = next_obj.name
            print(next_page)
            past_queue.append(Page(next_page, next_obj.parent, 0))
            total_pages += 1
            clicks_in_layer -= 1
            print(str(total_pages))

            # Code for if the target is reached
            if next_page == final_target:
                link = final_target
                print("Found final page, optimum clicks is: " + str(clicks))
                print("Total clicks: " + str(total_pages))

                click_path = []
                while link != "no--parent":
                    path_queue = past_queue
                    for i in path_queue:
                        if i.name == link:
                            click_path.append(i.name)
                            link = i.parent
                            break

                click_path.reverse()

                print("The click path is: " + str(click_path).replace('[', '').replace('\'', '').replace(']', ''))

                break

            weight, available_links = dictionary[next_page]
            if method == "BFS":
                for i in available_links:
                    future_queue.append(Page(i, next_page, 0))

            elif method == "BFS_no_repeats":
                for i in available_links:
                    exists = False
                    for i2 in future_queue:
                        if i2.name == i:
                            exists = True
                            break

                    if not exists:
                        for i2 in past_queue:
                            if i2.name == i:
                                exists = True
                                break
                    if not exists:
                        future_queue.append(Page(i, next_page, 0))

            elif method == "BFS_some_repeats":
                # some repeats is strange, there will be points where a link will be put onto the future queue
                # multiple times, however no infinite loops can occur. It saves time not searching the future
                # queue for instances of a page, but loses that time in the fact that there are some repeats
                # right now, I dont know which method is faster between this and no repeats

                for i in available_links:
                    print(i)
                    exists = False
                    for i2 in past_queue:
                        if i2.name == i:
                            exists = True
                            break
                    if not exists:
                        future_queue.append(Page(i, next_page, 0))

            if clicks_in_layer == 0:
                clicks += 1
                clicks_in_layer = len(future_queue)

        except KeyError:
            # Documentation of every broken link I encountered
            # This is inefficient code and ugly as hell, but i'm coding for my time efficiency as
            # at the final product stage this shouldn't be used much, if at all
            broken_link = open('BrokenLinks.txt', 'r')
            broken_link_list = [broken_link.readline().strip('\n')]
            while broken_link_list[len(broken_link_list) - 1] != "":
                broken_link_list.append(broken_link.readline().strip('\n'))
            broken_link.close()
            broken_link = open('BrokenLinks.txt', 'a')
            if next_page not in broken_link_list:
                print("Broken link found")
                broken_link.write(next_page + "\n")
                broken_link.close()
                num_broken_links += 1

    if next_page != final_target:
        print("Unable to reach the final target from this page")

    if num_broken_links > 0:
        print("Removed " + str(num_broken_links) + " broken links")
        broken_link_list.clear()


def weighted_bfs(dictionary, final_target, start_page, method):
    # This will only be done with one page, at present that page is: artificial intelligence
    num_broken_links = 0
    broken_link_list = []
    available_links = []
    weight = 0
    next_page = ""
    future_queue = deque()
    past_queue = deque()
    start = Page(start_page, "no--parent", int(4096))
    future_queue.append(start)
    clicks_in_layer = 1
    clicks = 0
    total_pages = 0
    while len(future_queue) > 0:
        try:
            next_obj = future_queue.popleft()
            exists = False
            if method == "weighted_BFS_some_repeats":
                for i in past_queue:
                    if i == next_obj:
                        exists = True
            if not exists:
                next_page = next_obj.name
                print(next_page)
                past_queue.append(Page(next_page, next_obj.parent, int(next_obj.weight)))
                total_pages += 1
                clicks_in_layer -= 1
                print(str(total_pages))

                # Code for if the target is reached
                if next_page == final_target:
                    link = final_target
                    print("Found final page, optimum clicks is: " + str(clicks))
                    print("Total clicks: " + str(total_pages))

                    click_path = []
                    while link != "no--parent":
                        path_queue = past_queue
                        for i in path_queue:
                            if i.name == link:
                                if i.weight > 2**len(click_path):
                                    i.weight = 2**len(click_path)
                                click_path.append(i.name)
                                link = i.parent
                                break

                    click_path.reverse()
                    print("The click path is: " + str(click_path).replace('[', '').replace('\'', '').replace(']', ''))
                    break

                non_used_weight, available_links = dictionary[next_page]

        except KeyError:
            # Documentation of every broken link I encountered
            # This is inefficient code and ugly as hell, but i'm coding for my time efficiency as
            # at the final product stage this shouldn't be used much, if at all
            broken_link = open('BrokenLinks.txt', 'r')
            broken_link_list = [broken_link.readline().strip('\n')]
            while broken_link_list[len(broken_link_list) - 1] != "":
                broken_link_list.append(broken_link.readline().strip('\n'))
            broken_link.close()
            broken_link = open('BrokenLinks.txt', 'a')
            if next_page not in broken_link_list:
                print("Broken link found")
                broken_link.write(next_page + "\n")
                broken_link.close()
                num_broken_links += 1
            print("Broken link found")

        if method == "weighted_BFS":
            for i in available_links:
                try:
                    weight, non_used_available_links = dictionary[i]
                except KeyError:
                    weight = "2048"
                finally:
                    future_queue.append(Page(i, next_page, int(weight)))

        elif method == "weighted_BFS_no_repeats":
            for i in available_links:
                exists = False
                for i2 in future_queue:
                    if i2.name == i:
                        exists = True
                        break

                if not exists:
                    for i2 in past_queue:
                        if i2.name == i:
                            exists = True
                            break
                if not exists:
                    try:
                        weight, non_used_available_links = dictionary[i]
                    except KeyError:
                        weight = "2048"

                    future_queue.append(Page(i, next_page, int(weight)))

        elif method == "weighted_BFS_some_repeats":
            # some repeats is strange, there will be points where a link will be put onto the future queue
            # multiple times, however no infinite loops can occur. It saves time not searching the future
            # queue for instances of a page, but loses that time in the fact that there are some repeats
            # right now, I dont know which method is faster between this and no repeats

            for i in available_links:
                exists = False
                for i2 in past_queue:
                    if i2.name == i:
                        exists = True
                        break
                if not exists:
                    try:
                        weight, non_used_available_links = dictionary[i]
                    except KeyError:
                        weight = "2048"

                    future_queue.append(Page(i, next_page, int(weight)))

        if clicks_in_layer == 0:
            clicks += 1
            clicks_in_layer = len(future_queue)

    if next_page != final_target:
        print("Unable to reach the final target from this page")

    if num_broken_links > 0:
        print("Removed " + str(num_broken_links) + " broken links")
        broken_link_list.clear()

    # write to a file the new weights
    update_weights = open("WeightedWiki.txt", 'w')
    for i in dictionary:
        weight, available_links = dictionary[i]
        for i2 in past_queue:
            if i == i2.name:
                weight = i2.weight
                for i3 in past_queue:
                    if i2.name == i3.parent:
                        if (i3.weight * 2) < i2.weight:
                            i2.weight = (i3.weight * 2)
                break

        update_weights.write(">" + i + "|" + str(weight))
        for i3 in available_links:
            update_weights.write("[" + i3)


def dijkstra(dictionary, final_target, start_page, method):
    future_queue = deque()
    past_queue = deque()
    weight, available_links = dictionary[start_page]

    future_queue.append(Node(start_page, "none", int(weight), float(0)))
    if weight == 2048 and method == "assign_weights_dijkstra":
        print("The final page cannot be reached from this page at the moment")
    else:
        next_page = start_page
        total_clicks = 0

        temp = Node("This will", "never be used", 0, 0)

        while next_page != final_target:
            for i in available_links:
                exists = False
                for i2 in future_queue:
                    if i2.name == i:
                        exists = True
                        break
                for i2 in past_queue:
                    if i2.name == i:
                        exists = True
                        break
                if not exists:
                    try:
                        weight, unused_available_links = dictionary[i]
                        future_queue.append(Node(i, next_page, weight, float("inf")))
                    except KeyError:
                        # This is just to shut the compiler up
                        exists = False
            total_clicks += 1
            queue_count = 0
            # get the next page from the future queue
            for i in future_queue:
                if i.name == next_page:
                    if queue_count != 0:
                        future_queue.rotate(queue_count)
                    temp = future_queue.popleft()
                    past_queue.append(temp)
                    break
                queue_count -= 1

            # update the links from next page with their new sizes
            for i in available_links:
                try:
                    weight, unused_available_links = dictionary[i]
                    for i2 in future_queue:
                        if i == i2.name:
                            if temp.size + float(weight) < i2.size:
                                i2.size = temp.size + float(weight)
                except KeyError:
                    weight = 0

            # find the next new page (the one with the smallest size)
            size = float("inf")
            for i in future_queue:
                if i.size < size:
                    size = i.size
                    next_page = i.name

            unused_weight, available_links = dictionary[next_page]
        if start_page == final_target:
            print("The start page and final page are the same")
        else:
            print(str(total_clicks) + " pages visited")
            back_page = temp.name
            clicks = 1
            click_path = [final_target]
            while back_page != start_page:
                click_path.append(back_page)
                clicks += 1
                for i in past_queue:
                    if i.name == temp.parent:
                        temp = i
                        break
                back_page = temp.name

            click_path.append(start_page)
            click_path.reverse()
            print("Found target, min clicks is: " + str(clicks))
            print("The click path is: " + str(click_path).replace('[', '').replace('\'', '').replace(']', ''))


def assign_weights(dictionary, final_target):
    # This function loops through the dictionary, assigning weights up to at least 10 clicks long, this should allow
    #  dijkstra's to function very well. I may make the clicks higher depending on how long 5 takes and how effective
    # 5 clicks is
    weight, unused_available_links = dictionary[final_target]
    # If the weight of the final target is 1, then it means the file is currently set up to have the final target
    # this means the calculations dont need to be run
    if not int(weight) == 1:
        # This resets the weights, which is needed for when the final target is changed
        for i in dictionary:
            unused_weight, available_links = dictionary[i]
            dictionary[i] = "2048", available_links

        pages_per_click = []
        unused_weight, temp = dictionary[final_target]
        dictionary[final_target] = 1, temp
        search_list = [final_target]
        next_list = []
        for clicks in range(0, 10):
            print(clicks)
            for i in dictionary:
                old_weight, available_links = dictionary[i]
                # This can be used since all links are set to 2048, and it gets passed over only after
                # having it's weight set
                if int(old_weight) > 2**clicks:
                    for i2 in search_list:
                        if i2 in available_links:
                            new_weight, unused_available_links = dictionary[i2]
                            if int(old_weight) > int(new_weight) * 2:
                                old_weight = int(new_weight) * 2
                                dictionary[i] = old_weight, available_links
                                next_list.append(i)

            search_list = next_list
            print(search_list)
            print(len(search_list))
            next_list = []

            pages_per_click.append(len(search_list))

        print(pages_per_click)
        # Writes them to a file for permanent storage, even after the code stops running
        update_weights = open("FullWeightedWiki.txt", 'w')
        for i in dictionary:
            weight, available_links = dictionary[i]
            update_weights.write(">" + i + "|" + str(weight))
            for i2 in available_links:
                update_weights.write("[" + i2)


def assign_weights2(dictionary, final_target, method):
    weight, unused_available_links = dictionary[final_target]
    # If the weight of the final target is 1, then it means the file is currently set up to have the final target
    # this means the calculations dont need to be run

    # This version of assign weights should be faster as it loops through dictionary 10 times with the available links
    # for every item. The other version loops through dictionary 10 times with available links and the search list
    if not int(weight) == 1:
        # This resets the weights, which is needed for when the final target is changed

        for i in dictionary:
            unused_weight, available_links = dictionary[i]
            dictionary[i] = "2048", available_links

        for clicks in range(1, 11):
            pages_per_click = []
            unused_weight, temp = dictionary[final_target]
            dictionary[final_target] = 1, temp
            for i in dictionary:
                old_weight, available_links = dictionary[i]
                if int(old_weight) > 2**clicks:
                    new_weight = 2048
                    for i2 in available_links:
                        try:
                            weight, unused_available_links = dictionary[i2]
                            if int(weight) * 2 < int(new_weight):
                                new_weight = int(weight) * 2
                        except KeyError:
                            weight = 0
                    dictionary[i] = new_weight, available_links

        if method == "assign_weights":
            print("Weights assigned, storing in text file")
            # Writes them to a file for permanent storage, even after the code stops running
            update_weights = open("FullWeightedWiki.txt", 'w')
            for i in dictionary:
                weight, available_links = dictionary[i]
                update_weights.write(">" + i + "|" + str(weight))
                for i2 in available_links:
                    update_weights.write("[" + i2)
        else:
            return dictionary


if __name__ == '__main__':
    main()
