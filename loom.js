class LoomComponent {
    constructor(styles, events, render) {
        this.styles = styles;
        this.events = events;
        this.render = render;
    }
}

class Loom {
    constructor() {
        this.components = {};
        this.root = document.createElement('div');
        document.body.appendChild(this.root);
    }

    defineComponent(name, component) {
        this.components[name] = component;
    }

    renderComponent(name, root) {
        const component = this.components[name];
        if (!component) {
            console.error(`Component ${name} not found`);
            return;
        }

        const element = this.createElement(component.render());
        this.applyStyles(element, component.styles);
        this.applyEvents(element, component.events);
        root.appendChild(element);
    }

    createElement(renderFunc) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = renderFunc.trim();
        return tempDiv.firstChild;
    }

    applyStyles(element, styles) {
        Object.assign(element.style, styles);
    }

    applyEvents(element, events) {
        for (const event in events) {
            element.addEventListener(event.toLowerCase(), events[event]);
        }
    }

    start() {
        document.addEventListener('DOMContentLoaded', () => {
            this.renderComponent('App', this.root);
        });
    }
}

window.Loom = Loom;
window.LoomComponent = LoomComponent;

