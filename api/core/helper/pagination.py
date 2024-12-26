import math


class Pagination:
    def __init__(self, item_list, per_page):
        self.item_list = item_list
        self.per_page = per_page
        self.total_items = len(item_list)
        self.total_pages = math.ceil(self.total_items / per_page)

    def getPage(self, pageno):
        pageno = pageno if pageno < self.total_pages else self.total_pages
        from_no = (pageno - 1) * self.per_page
        if pageno == self.total_pages and self.total_items % self.per_page > 0:
            to_no = (pageno * self.per_page) - self.total_items % self.per_page
        else:
            to_no = pageno * self.per_page
        next_page = pageno + 1 if pageno < self.total_pages else self.total_pages
        previous_page = pageno - 1 if pageno != 1 else 1
        show_next = False if (pageno == self.total_pages) else True
        show_previous = False if (pageno == 1) else True
        return {
            "results": self.item_list[from_no:to_no],
            "controls": {
                "total_pages": self.total_pages,
                "show_next": show_next,
                "show_previous": show_previous,
                "total_items": self.total_items,
                "current_page": pageno,
                "next_page": next_page,
                "previous_page": previous_page
            }
        }
