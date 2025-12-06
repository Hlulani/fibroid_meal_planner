from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Meal:
    id: str
    name: str
    meal_type: str  # "breakfast" | "lunch" | "dinner" | "snack"

    tags: List[str] = field(default_factory=list)

    anti_inflammatory_score: int = 1  # 1 = very anti inflammatory, 10 = very inflammatory
    iron_support: int = 0             # 0 to 5
    fiber_score: int = 0              # 0 to 5
    max_repeats_per_30: int = 4       # to avoid repeating too often

    ingredients: List[Dict[str, str]] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)


MEALS: List[Meal] = [

    # =========================
    # BREAKFASTS (7)
    # =========================

    Meal(
        id="b_oats_berries_chia",
        name="Anti inflammatory oats with berries and chia",
        meal_type="breakfast",
        tags=["anti_inflammatory", "high_fiber", "fibroid_friendly", "hormone_support"],
        anti_inflammatory_score=1,
        iron_support=2,
        fiber_score=4,
        ingredients=[
            {"item": "Rolled oats", "amount": "1/2 cup"},
            {"item": "Water or unsweetened almond milk", "amount": "1 cup"},
            {"item": "Chia seeds", "amount": "1 tbsp"},
            {"item": "Mixed berries (fresh or frozen)", "amount": "1/2 cup"},
            {"item": "Cinnamon", "amount": "1/4 tsp"},
            {"item": "Honey or maple syrup (optional)", "amount": "1 tsp"},
        ],
        instructions=[
            "Bring the water or almond milk to a gentle simmer.",
            "Add oats and cook for 5 to 8 minutes, stirring, until soft and creamy.",
            "Stir in chia seeds and cinnamon.",
            "Serve in a bowl and top with berries.",
            "Drizzle a small amount of honey or maple syrup if you like.",
        ],
    ),

    Meal(
        id="b_green_smoothie_flax",
        name="Spinach, flax and ginger hormone support smoothie",
        meal_type="breakfast",
        tags=["anti_inflammatory", "liver_support", "high_fiber", "fibroid_friendly"],
        anti_inflammatory_score=1,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Fresh spinach", "amount": "2 cups"},
            {"item": "Frozen banana", "amount": "1 small"},
            {"item": "Ground flaxseed", "amount": "1 tbsp"},
            {"item": "Fresh ginger, grated", "amount": "1 tsp"},
            {"item": "Water or unsweetened almond milk", "amount": "250 ml"},
            {"item": "Ice cubes (optional)", "amount": "2 to 3"},
        ],
        instructions=[
            "Add spinach, banana, flaxseed, ginger and liquid to a blender.",
            "Blend until completely smooth.",
            "Add a little more water if you prefer a thinner texture.",
            "Pour into a glass and serve cold.",
        ],
    ),

    Meal(
        id="b_golden_oat_porridge",
        name="Cinnamon turmeric golden oat porridge",
        meal_type="breakfast",
        tags=["anti_inflammatory", "hormone_support"],
        anti_inflammatory_score=1,
        iron_support=1,
        fiber_score=3,
        ingredients=[
            {"item": "Rolled oats", "amount": "1/2 cup"},
            {"item": "Unsweetened almond milk", "amount": "1 cup"},
            {"item": "Turmeric powder", "amount": "1/4 tsp"},
            {"item": "Cinnamon", "amount": "1/4 tsp"},
            {"item": "Ground black pepper", "amount": "a pinch"},
            {"item": "Honey (optional)", "amount": "1 tsp"},
        ],
        instructions=[
            "Add oats and almond milk to a small pot and bring to a simmer.",
            "Stir in turmeric, cinnamon and a small pinch of black pepper.",
            "Cook for 5 to 7 minutes until creamy.",
            "Remove from heat and sweeten lightly with honey if desired.",
        ],
    ),

    Meal(
        id="b_yoghurt_parfait",
        name="Greek yoghurt berry parfait bowl",
        meal_type="breakfast",
        tags=["high_protein", "gut_support", "anti_inflammatory"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Plain Greek yoghurt", "amount": "3/4 cup"},
            {"item": "Mixed berries", "amount": "1/2 cup"},
            {"item": "Pumpkin seeds", "amount": "1 tbsp"},
            {"item": "Cinnamon", "amount": "a pinch"},
        ],
        instructions=[
            "Spoon Greek yoghurt into a bowl or glass.",
            "Layer berries on top.",
            "Sprinkle pumpkin seeds over the berries.",
            "Dust with a little cinnamon before serving.",
        ],
    ),

    Meal(
        id="b_apple_cinnamon_overnight_oats",
        name="Cinnamon apple overnight oats",
        meal_type="breakfast",
        tags=["high_fiber", "anti_inflammatory"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=4,
        ingredients=[
            {"item": "Rolled oats", "amount": "1/2 cup"},
            {"item": "Unsweetened almond milk", "amount": "1 cup"},
            {"item": "Apple, grated", "amount": "1/2 medium"},
            {"item": "Chia seeds", "amount": "1 tbsp"},
            {"item": "Cinnamon", "amount": "1/2 tsp"},
        ],
        instructions=[
            "Add oats, almond milk, grated apple, chia seeds and cinnamon to a jar.",
            "Stir well, cover and place in the fridge overnight.",
            "Give it a stir in the morning and eat cold or gently warmed.",
        ],
    ),

    Meal(
        id="b_savory_mediterranean_egg_bowl",
        name="Savory Mediterranean egg bowl",
        meal_type="breakfast",
        tags=["high_protein", "anti_inflammatory", "hormone_support"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=1,
        ingredients=[
            {"item": "Eggs", "amount": "2"},
            {"item": "Fresh spinach", "amount": "1/2 cup"},
            {"item": "Cherry tomatoes, halved", "amount": "5"},
            {"item": "Olives, sliced (optional)", "amount": "1 tbsp"},
            {"item": "Olive oil", "amount": "1 tsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Heat olive oil in a small pan over medium heat.",
            "Add spinach and cherry tomatoes and cook until spinach wilts.",
            "Beat eggs in a bowl, season with salt and pepper and pour into the pan.",
            "Cook, stirring gently, until the eggs are just set.",
            "Top with sliced olives if using and serve warm.",
        ],
    ),

    Meal(
        id="b_buckwheat_berry_pancakes",
        name="Buckwheat pancakes with berries",
        meal_type="breakfast",
        tags=["high_fiber", "anti_inflammatory"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=3,
        ingredients=[
            {"item": "Buckwheat flour", "amount": "1/2 cup"},
            {"item": "Egg", "amount": "1"},
            {"item": "Unsweetened almond milk", "amount": "1/3 cup (plus more if needed)"},
            {"item": "Baking powder", "amount": "1/2 tsp"},
            {"item": "Fresh or frozen berries", "amount": "1/4 cup"},
            {"item": "Olive or coconut oil for the pan", "amount": "1 tsp"},
        ],
        instructions=[
            "Whisk buckwheat flour and baking powder in a bowl.",
            "Add the egg and almond milk and mix into a smooth batter; add a splash more milk if too thick.",
            "Fold in the berries gently.",
            "Heat a little oil in a non-stick pan over medium heat.",
            "Cook small pancakes for about 2 to 3 minutes per side until golden and cooked through.",
        ],
    ),

    # =========================
    # LUNCHES (8)
    # =========================

    Meal(
        id="l_chickpea_buddha_bowl",
        name="Chickpea Buddha bowl with turmeric tahini",
        meal_type="lunch",
        tags=["anti_inflammatory", "high_fiber", "iron_rich", "fibroid_friendly"],
        anti_inflammatory_score=2,
        iron_support=3,
        fiber_score=4,
        ingredients=[
            {"item": "Cooked chickpeas", "amount": "1 cup"},
            {"item": "Broccoli florets", "amount": "1 cup"},
            {"item": "Sweet potato, cubed", "amount": "1 medium"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Paprika", "amount": "1/2 tsp"},
            {"item": "Salt", "amount": "to taste"},
            {"item": "Turmeric", "amount": "1/2 tsp"},
            {"item": "Black pepper", "amount": "a pinch"},
            {"item": "Tahini", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tbsp"},
        ],
        instructions=[
            "Preheat the oven to 200°C.",
            "Toss broccoli and sweet potato cubes with half of the olive oil, paprika and salt.",
            "Spread on a baking tray and roast for 20 to 25 minutes until tender.",
            "In a small pan, warm chickpeas with turmeric, black pepper and a pinch of salt.",
            "In a bowl, whisk tahini with lemon juice and a splash of water until it forms a pourable sauce.",
            "Assemble the bowl with chickpeas, roasted vegetables and drizzle with the tahini lemon sauce.",
        ],
    ),

    Meal(
        id="l_warm_mediterranean_lentil_salad",
        name="Warm Mediterranean lentil salad",
        meal_type="lunch",
        tags=["anti_inflammatory", "high_fiber", "iron_rich"],
        anti_inflammatory_score=2,
        iron_support=3,
        fiber_score=3,
        ingredients=[
            {"item": "Cooked brown or green lentils", "amount": "1 cup"},
            {"item": "Cucumber, diced", "amount": "1/2 medium"},
            {"item": "Cherry tomatoes, halved", "amount": "6 to 8"},
            {"item": "Red onion, finely chopped", "amount": "2 tbsp"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tbsp"},
            {"item": "Dried oregano", "amount": "1/2 tsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Place warm lentils in a bowl.",
            "Add cucumber, cherry tomatoes and chopped red onion.",
            "In a small bowl, whisk olive oil, lemon juice, oregano, salt and pepper.",
            "Pour the dressing over the lentil mixture and toss gently.",
        ],
    ),

    Meal(
        id="l_quinoa_avocado_salad",
        name="Quinoa salad with avocado and greens",
        meal_type="lunch",
        tags=["anti_inflammatory", "hormone_support", "high_fiber"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=3,
        ingredients=[
            {"item": "Cooked quinoa", "amount": "1 cup"},
            {"item": "Mixed salad greens", "amount": "2 cups"},
            {"item": "Avocado, diced", "amount": "1/2"},
            {"item": "Cucumber, diced", "amount": "1/2 medium"},
            {"item": "Cherry tomatoes, halved", "amount": "6"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tbsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Combine salad greens, cucumber and cherry tomatoes in a bowl.",
            "Add cooked quinoa and diced avocado.",
            "Drizzle with olive oil and lemon juice.",
            "Season with salt and pepper and toss gently.",
        ],
    ),

    Meal(
        id="l_simple_tuna_salad_plate",
        name="Simple tuna salad plate",
        meal_type="lunch",
        tags=["high_protein", "anti_inflammatory"],
        anti_inflammatory_score=3,
        iron_support=2,
        fiber_score=1,
        ingredients=[
            {"item": "Canned tuna in water, drained", "amount": "1/2 can"},
            {"item": "Olive oil", "amount": "1 tsp"},
            {"item": "Lemon juice", "amount": "1 tsp"},
            {"item": "Lettuce or mixed greens", "amount": "1 cup"},
            {"item": "Corn kernels (optional)", "amount": "1/4 cup"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Mix drained tuna with olive oil, lemon juice, salt and pepper.",
            "Arrange lettuce or mixed greens on a plate.",
            "Spoon tuna mixture over the greens and sprinkle with corn if using.",
        ],
    ),

    Meal(
        id="l_moroccan_chickpea_soup",
        name="Moroccan inspired chickpea soup",
        meal_type="lunch",
        tags=["anti_inflammatory", "high_fiber", "iron_rich"],
        anti_inflammatory_score=2,
        iron_support=3,
        fiber_score=3,
        ingredients=[
            {"item": "Onion, chopped", "amount": "1/2 medium"},
            {"item": "Carrot, chopped", "amount": "1 medium"},
            {"item": "Cooked chickpeas", "amount": "1 cup"},
            {"item": "Tomato paste", "amount": "1 tbsp"},
            {"item": "Ground cumin", "amount": "1 tsp"},
            {"item": "Ground coriander (optional)", "amount": "1/2 tsp"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Vegetable broth or water", "amount": "2 cups"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Heat olive oil in a pot and sauté onion and carrot until softened.",
            "Stir in tomato paste, cumin and coriander and cook for a minute.",
            "Add chickpeas and broth.",
            "Simmer for 15 to 20 minutes, adding more liquid if needed.",
            "Season with salt and pepper.",
        ],
    ),

    Meal(
        id="l_sweet_potato_kale_bowl",
        name="Sweet potato and kale nourish bowl",
        meal_type="lunch",
        tags=["anti_inflammatory", "high_fiber", "fibroid_friendly"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=4,
        ingredients=[
            {"item": "Sweet potato, cubed", "amount": "1 cup"},
            {"item": "Kale, stems removed and chopped", "amount": "1 cup"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tbsp"},
            {"item": "Pumpkin seeds", "amount": "1 tbsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Preheat oven to 200°C.",
            "Toss sweet potato cubes with half the olive oil, salt and pepper and roast for 20 to 25 minutes until tender.",
            "Place chopped kale in a bowl and massage with remaining olive oil, lemon juice, salt and pepper until slightly softened.",
            "Top the kale with roasted sweet potatoes and sprinkle with pumpkin seeds.",
        ],
    ),

    Meal(
        id="l_broccoli_tahini_protein_bowl",
        name="Broccoli tahini protein bowl",
        meal_type="lunch",
        tags=["anti_inflammatory", "high_fiber"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Broccoli florets", "amount": "1 cup"},
            {"item": "Cooked quinoa or brown rice", "amount": "1/2 cup"},
            {"item": "Boiled egg", "amount": "1"},
            {"item": "Tahini", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tbsp"},
            {"item": "Water", "amount": "1 to 2 tbsp (to thin tahini)"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Steam broccoli until just tender but still bright green.",
            "Place cooked quinoa or brown rice in a bowl and top with broccoli and sliced boiled egg.",
            "In a small bowl, whisk tahini, lemon juice, a pinch of salt and enough water to make a pourable sauce.",
            "Drizzle the tahini sauce over the bowl and season with extra salt and pepper if needed.",
        ],
    ),

    Meal(
        id="l_avocado_salmon_rice_bowl",
        name="Avocado salmon rice bowl",
        meal_type="lunch",
        tags=["anti_inflammatory", "omega3"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=2,
        ingredients=[
            {"item": "Cooked brown rice", "amount": "1/2 to 3/4 cup"},
            {"item": "Cooked salmon, flaked", "amount": "1/2 cup"},
            {"item": "Avocado, diced", "amount": "1/3 medium"},
            {"item": "Spring onion, sliced", "amount": "1 tbsp"},
            {"item": "Lemon or lime juice", "amount": "1 tsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Place warm brown rice in a bowl.",
            "Top with salmon flakes, diced avocado and spring onion.",
            "Season with lemon or lime juice, salt and pepper.",
        ],
    ),

    # =========================
    # DINNERS (8)
    # =========================

    Meal(
        id="d_salmon_broccoli_sweet_potato",
        name="Baked salmon with broccoli and sweet potato",
        meal_type="dinner",
        tags=["anti_inflammatory", "omega3", "cruciferous", "fibroid_friendly"],
        anti_inflammatory_score=1,
        iron_support=2,
        fiber_score=2,
        ingredients=[
            {"item": "Salmon fillet", "amount": "150 to 180 g"},
            {"item": "Broccoli florets", "amount": "1 to 1.5 cups"},
            {"item": "Sweet potato, cubed", "amount": "1 medium"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
            {"item": "Lemon wedge (optional)", "amount": "1"},
        ],
        instructions=[
            "Preheat oven to 180 to 200°C.",
            "Place salmon, broccoli and sweet potato on a baking tray.",
            "Drizzle with olive oil and season with salt and pepper.",
            "Bake for 20 to 25 minutes until salmon flakes easily and vegetables are tender.",
            "Serve with a squeeze of lemon if you like.",
        ],
    ),

    Meal(
        id="d_peanut_sweet_potato_stew",
        name="Peanut sweet potato stew with spinach",
        meal_type="dinner",
        tags=["anti_inflammatory", "high_fiber", "fibroid_friendly"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Sweet potato, peeled and cubed", "amount": "1 cup"},
            {"item": "Natural peanut butter", "amount": "2 tbsp"},
            {"item": "Tomato paste", "amount": "1 tbsp"},
            {"item": "Fresh spinach", "amount": "2 cups"},
            {"item": "Onion, chopped", "amount": "1/2 medium"},
            {"item": "Garlic, minced", "amount": "1 clove"},
            {"item": "Fresh ginger, grated", "amount": "1 tsp"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Water or vegetable broth", "amount": "2 cups"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Heat olive oil in a pot and sauté onion, garlic and ginger until fragrant.",
            "Add sweet potato cubes and stir.",
            "Whisk peanut butter and tomato paste into the water or broth and pour into the pot.",
            "Simmer until sweet potatoes are soft, about 15 to 20 minutes.",
            "Stir in spinach and cook until wilted.",
            "Season with salt and pepper before serving.",
        ],
    ),

    Meal(
        id="d_coconut_curry_chickpeas",
        name="Coconut curry chickpeas with spinach",
        meal_type="dinner",
        tags=["anti_inflammatory", "high_fiber"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Cooked chickpeas", "amount": "1 cup"},
            {"item": "Coconut milk", "amount": "1/2 cup"},
            {"item": "Water or vegetable broth", "amount": "1/2 cup"},
            {"item": "Curry paste or curry powder", "amount": "1 tsp"},
            {"item": "Fresh spinach", "amount": "1 cup"},
            {"item": "Onion, chopped", "amount": "1/2 medium"},
            {"item": "Garlic, minced", "amount": "1 clove"},
            {"item": "Olive or coconut oil", "amount": "1 tbsp"},
            {"item": "Salt", "amount": "to taste"},
        ],
        instructions=[
            "Heat oil in a pan and sauté onion and garlic until soft.",
            "Stir in curry paste or powder and cook for 1 minute.",
            "Add chickpeas, coconut milk and water or broth.",
            "Simmer for 10 to 15 minutes.",
            "Stir in spinach until wilted and season with salt.",
        ],
    ),

    Meal(
        id="d_spicy_lentil_dahl",
        name="Spicy red lentil dahl",
        meal_type="dinner",
        tags=["anti_inflammatory", "high_fiber", "iron_rich"],
        anti_inflammatory_score=2,
        iron_support=4,
        fiber_score=4,
        ingredients=[
            {"item": "Red lentils, rinsed", "amount": "3/4 cup"},
            {"item": "Coconut milk", "amount": "1/4 cup"},
            {"item": "Water or vegetable broth", "amount": "2 cups"},
            {"item": "Turmeric", "amount": "1/2 tsp"},
            {"item": "Ground cumin", "amount": "1/2 tsp"},
            {"item": "Fresh ginger, grated", "amount": "1 tsp"},
            {"item": "Garlic, minced", "amount": "1 clove"},
            {"item": "Onion, chopped", "amount": "1/2 medium"},
            {"item": "Olive or coconut oil", "amount": "1 tbsp"},
            {"item": "Salt", "amount": "to taste"},
        ],
        instructions=[
            "Heat oil in a pot and sauté onion, garlic and ginger until soft.",
            "Add lentils, water or broth, turmeric and cumin.",
            "Bring to a boil, then reduce heat and simmer for 15 to 20 minutes until lentils are soft.",
            "Stir in coconut milk and season with salt.",
        ],
    ),

    Meal(
        id="d_creamy_cauliflower_soup",
        name="Creamy cauliflower soup",
        meal_type="dinner",
        tags=["anti_inflammatory", "fibroid_friendly"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Cauliflower florets", "amount": "2 cups"},
            {"item": "Onion, chopped", "amount": "1/2 medium"},
            {"item": "Garlic, minced", "amount": "1 clove"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Vegetable broth", "amount": "1.5 cups"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Heat olive oil in a pot and sauté onion and garlic until soft.",
            "Add cauliflower florets and stir for a minute.",
            "Pour in vegetable broth, bring to a boil, then simmer until cauliflower is tender.",
            "Blend until smooth and season with salt and pepper.",
        ],
    ),

    Meal(
        id="d_veggie_tofu_stir_fry",
        name="Vegetable and tofu stir fry",
        meal_type="dinner",
        tags=["anti_inflammatory", "high_fiber"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Firm tofu, cubed", "amount": "1/2 block"},
            {"item": "Broccoli florets", "amount": "1 cup"},
            {"item": "Red bell pepper, sliced", "amount": "1/2"},
            {"item": "Carrot, sliced", "amount": "1 small"},
            {"item": "Fresh ginger, grated", "amount": "1 tsp"},
            {"item": "Garlic, minced", "amount": "1 clove"},
            {"item": "Olive or avocado oil", "amount": "1 tbsp"},
            {"item": "Tamari or low sodium soy sauce", "amount": "1 tbsp"},
        ],
        instructions=[
            "Heat oil in a large pan or wok over medium-high heat.",
            "Add tofu cubes and cook until lightly browned on all sides, then remove from the pan.",
            "In the same pan, sauté ginger and garlic for 1 minute.",
            "Add broccoli, bell pepper and carrot and stir fry until just tender.",
            "Return tofu to the pan, pour in tamari or soy sauce and toss everything together.",
        ],
    ),

    Meal(
        id="d_garlic_lemon_roast_chicken",
        name="Garlic lemon roasted chicken",
        meal_type="dinner",
        tags=["anti_inflammatory", "high_protein"],
        anti_inflammatory_score=3,
        iron_support=2,
        fiber_score=0,
        ingredients=[
            {"item": "Chicken thighs, bone in", "amount": "2 pieces"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Garlic cloves, minced", "amount": "3"},
            {"item": "Lemon, sliced or juiced", "amount": "1/2"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Preheat oven to 190°C.",
            "Rub chicken thighs with olive oil, minced garlic, salt and pepper.",
            "Place in a baking dish and top with lemon slices or squeeze lemon juice over.",
            "Roast for 30 to 40 minutes until cooked through and the skin is crisp.",
        ],
    ),

    Meal(
        id="d_mediterranean_fish_bake",
        name="Mediterranean fish bake with tomatoes and olives",
        meal_type="dinner",
        tags=["anti_inflammatory", "omega3"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=1,
        ingredients=[
            {"item": "White fish fillet (such as hake or cod)", "amount": "1 fillet"},
            {"item": "Cherry tomatoes", "amount": "8 to 10"},
            {"item": "Pitted olives, sliced (optional)", "amount": "2 tbsp"},
            {"item": "Olive oil", "amount": "1 tbsp"},
            {"item": "Dried oregano", "amount": "1/2 tsp"},
            {"item": "Salt and pepper", "amount": "to taste"},
        ],
        instructions=[
            "Preheat oven to 180°C.",
            "Place fish in a small baking dish and scatter cherry tomatoes and olives around it.",
            "Drizzle with olive oil and sprinkle with oregano, salt and pepper.",
            "Bake for 15 to 18 minutes or until the fish is opaque and flakes easily.",
        ],
    ),

    # =========================
    # SNACKS (7)
    # =========================

    Meal(
        id="s_nuts_apple",
        name="Nut and apple fiber snack",
        meal_type="snack",
        tags=["anti_inflammatory", "high_fiber"],
        anti_inflammatory_score=1,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Raw almonds or mixed nuts", "amount": "1 small handful"},
            {"item": "Apple, sliced", "amount": "1 medium"},
        ],
        instructions=[
            "Slice the apple.",
            "Serve the apple slices with a small handful of nuts.",
        ],
    ),

    Meal(
        id="s_hummus_veg",
        name="Hummus with raw veggie sticks",
        meal_type="snack",
        tags=["anti_inflammatory", "high_fiber", "easy"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Hummus", "amount": "3 to 4 tbsp"},
            {"item": "Carrot sticks", "amount": "1/2 cup"},
            {"item": "Cucumber sticks", "amount": "1/2 cup"},
            {"item": "Red pepper strips (optional)", "amount": "1/4 cup"},
        ],
        instructions=[
            "Slice carrot, cucumber and red pepper into sticks.",
            "Serve with a portion of hummus for dipping.",
        ],
    ),

    Meal(
        id="s_greek_yoghurt_berries",
        name="Greek yoghurt and berries snack",
        meal_type="snack",
        tags=["high_protein", "anti_inflammatory"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=1,
        ingredients=[
            {"item": "Plain Greek yoghurt", "amount": "1/2 cup"},
            {"item": "Mixed berries", "amount": "1/3 cup"},
        ],
        instructions=[
            "Spoon Greek yoghurt into a small bowl.",
            "Top with mixed berries and enjoy.",
        ],
    ),

    Meal(
        id="s_roasted_chickpeas",
        name="Crunchy roasted chickpeas",
        meal_type="snack",
        tags=["high_fiber", "anti_inflammatory"],
        anti_inflammatory_score=2,
        iron_support=2,
        fiber_score=3,
        ingredients=[
            {"item": "Cooked chickpeas, drained and dried", "amount": "1 cup"},
            {"item": "Olive oil", "amount": "1 tsp"},
            {"item": "Paprika", "amount": "1/2 tsp"},
            {"item": "Garlic powder (optional)", "amount": "1/4 tsp"},
            {"item": "Salt", "amount": "to taste"},
        ],
        instructions=[
            "Preheat oven to 190°C.",
            "Toss chickpeas with olive oil, paprika, garlic powder and salt.",
            "Spread on a baking tray and roast for 20 to 30 minutes until crispy, shaking the tray once or twice.",
        ],
    ),

    Meal(
        id="s_orange_almonds",
        name="Orange and almonds snack",
        meal_type="snack",
        tags=["anti_inflammatory", "easy"],
        anti_inflammatory_score=1,
        iron_support=1,
        fiber_score=1,
        ingredients=[
            {"item": "Orange, peeled and segmented", "amount": "1 medium"},
            {"item": "Raw almonds", "amount": "8 to 10"},
        ],
        instructions=[
            "Peel and segment the orange.",
            "Serve with a small handful of almonds.",
        ],
    ),

    Meal(
        id="s_trail_mix",
        name="Simple anti-inflammatory trail mix",
        meal_type="snack",
        tags=["anti_inflammatory", "easy"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Raw almonds", "amount": "2 tbsp"},
            {"item": "Raw walnuts", "amount": "2 tbsp"},
            {"item": "Unsweetened dried cranberries or raisins", "amount": "1 tbsp"},
            {"item": "Pumpkin seeds", "amount": "1 tbsp"},
        ],
        instructions=[
            "Combine almonds, walnuts, dried fruit and pumpkin seeds in a small container.",
            "Mix and store as a ready to grab snack.",
        ],
    ),

    Meal(
        id="s_carrot_tahini_dip",
        name="Carrot sticks with lemon tahini dip",
        meal_type="snack",
        tags=["anti_inflammatory", "high_fiber"],
        anti_inflammatory_score=2,
        iron_support=1,
        fiber_score=2,
        ingredients=[
            {"item": "Carrots, cut into sticks", "amount": "1 to 2 small carrots"},
            {"item": "Tahini", "amount": "1 tbsp"},
            {"item": "Lemon juice", "amount": "1 tsp"},
            {"item": "Water", "amount": "1 to 2 tsp (to thin)"},
            {"item": "Salt", "amount": "a pinch"},
        ],
        instructions=[
            "In a small bowl, whisk tahini, lemon juice, salt and enough water to make a smooth dip.",
            "Serve carrot sticks with the tahini dip on the side.",
        ],
    ),

]
