
import axiomic as ax


def test_load_save_txt():
    filename = '/tmp/hello_world.ax'
    agent = ax.Text('Hello, World!')
    ax.save(agent, filename)
    loaded = ax.load(filename)
    assert 'Hello, World!' == loaded.value()


def test_load_infer():
    filename = '/tmp/hello_world.ax'
    templ = ax.Text('What is the opposite of {thing}?')
    ans = templ.format(thing='up').infer()
    ax.save(ans, filename)
    loaded = ax.load(filename)
    assert 'down' in loaded.value().lower()

