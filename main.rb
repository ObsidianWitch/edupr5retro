require "gosu"

class Game < Gosu::Window
    def initialize()
        super(640, 480)
        self.caption = "Pacman"
        @font = Gosu::Font.new(50)
    end

    def update
    end

    def draw
        str = "World"
        @font.draw(
            text    = "Hello, #{str}",
            x       = 10,
            y       = 10,
            z       = 0,
            scale_x = 1.0,
            scale_y = 1.0,
            color   = Gosu::Color::YELLOW,
        )
    end
end

Game.new().show()
