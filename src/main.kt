package pacman

import com.badlogic.gdx.Gdx.gl
import com.badlogic.gdx.ApplicationAdapter
import com.badlogic.gdx.graphics.Color
import com.badlogic.gdx.graphics.GL20
import com.badlogic.gdx.graphics.g2d.BitmapFont
import com.badlogic.gdx.graphics.g2d.SpriteBatch
import com.badlogic.gdx.backends.lwjgl.LwjglApplication

class Game : ApplicationAdapter() {
    private lateinit var batch: SpriteBatch
    private lateinit var font: BitmapFont

    override fun create() {
        batch = SpriteBatch()
        font = BitmapFont().apply {
            setColor(Color.RED)
        }
        gl.glClearColor(0f, 0f, 0f, 0f)
    }

    override fun dispose() {
        batch.dispose()
        font.dispose()
    }

    override fun render() {
        gl.glClear(GL20.GL_COLOR_BUFFER_BIT)

        val l = 1
        batch.begin()
        font.draw(batch, "He${l}${l}o Wor${l}d", 200f, 200f)
        batch.end()
    }
}

fun main(args: Array<String>) {
    LwjglApplication(Game())
}
