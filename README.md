# django_components

Componentização estilo React no Django, simples e fácil

Estrutura dos arquivos

```raw
templates/
-- home.html
-- components/
---- container.html
---- button.html
```

Configuração:
```python
INSTALLED_APPS = [
  ...
  'django_components',
  ...
]
```

Templates e componentes.

**home.html**
```django
  {% load django_components %}
  
  {% component_block "container" name="Gilson Fabiano" %}
    <div> My text </div>
    {% component "button" text="Its works :)" %}
    {% component "button" text="Hehe!" %}
  {% endcomponent_block %}
    
```

**container.html**
```django
<div>
    <h1>Hello, i'm {{ props.name }}</h1>
    <div>{{ props.children }}</div>
</div>
```

**button.html**
```django
  <button type="button">{{ props.text }}</button>
```

**output:**
```html
  <div>
    <h1>Hello, i'm Gilson Fabiano</h1>
    <div>
        <div> My text </div>
        <button type="button">Its works :)</button>
        <button type="button">Hehe!</button>
    </div>
  </div>
```

## Notas
* A resolução do nome é feito automáticamente usando o sistema de busca de template padrão do Django seguindo o padrão: `components/%s.html`
