world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI
collision_pairs = {}

def add_oject(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            break
    remove_collision_object(o)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        for objects in pairs:
            while o in objects:
                objects.remove(o)

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()




def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def add_collision_pairs(group, a, b):
    if group not in collision_pairs: # 처음 등록되는 그룹이면, 충돌 쌍을 위한 리스트를 생성
        collision_pairs[group] = ([], []) # a와 b를 위한 리스트를 각각 생성
    if a is not None:
        collision_pairs[group][0].append(a)
    if b is not None:
        collision_pairs[group][1].append(b)

def handle_collision():
    for group, pairs in collision_pairs.items():
        # 충돌 처리 중 객체가 삭제되어도 다음 객체를 건너뛰지 않는다.
        for a in pairs[0][:]:
            for b in pairs[1][:]:
                if a in pairs[0] and b in pairs[1] and collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
