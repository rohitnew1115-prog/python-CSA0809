"""Q5: Canteen order functions, parameters, mutability and scope."""
def add_item_buggy(item, order=[]):
    order.append(item); return order
def add_item(item, order=None):
    if order is None: order=[]
    order.append(item); return order
def create_order(customer, items, tax_rate=0.05):
    copied=list(items); subtotal=sum(price for _,price in copied); tax=subtotal*tax_rate
    return customer, copied, subtotal, tax, subtotal+tax
def add_one_global():
    global global_counter
    global_counter += 1; return global_counter
def make_counter():
    count=0
    def increment():
        nonlocal count
        count += 1; return count
    return increment
def main():
    print("Shared mutable default:",add_item_buggy("Tea"),add_item_buggy("Vada"))
    print("None default creates fresh lists:",add_item("Tea"),add_item("Vada"))
    orders=[create_order("Asha",[("Tea",10),("Idli",30)]),create_order("Bala",[("Coffee",20)]),create_order("Charan",[("Vada",15),("Dosa",40)],tax_rate=0.05)]
    for order in orders: print("customer, items, subtotal, tax, total =",order)
    global global_counter; global_counter=0
    print("global:",add_one_global()); counter=make_counter(); print("closure/nonlocal:",counter(),counter())
    print("Positional arguments follow parameter order; keyword arguments name parameters; tax_rate is optional/defaulted.")
    print("Tuple return provides five values; named data classes/dicts are another readable option.")
    print("Avoid globals because hidden shared state harms testing/reuse; prefer explicit state or per-customer closures.")
    print("List append amortised O(1); storing m items uses O(m) space.")
if __name__ == '__main__': main()
