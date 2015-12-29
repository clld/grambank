<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%inherit file="../home_comp.mako"/>

<h3>Dependencies</h3>


<div class="span4 alert">
    <img src="${request.static_url('grambank:static/dependencies.png')}">
    <div>
        <small>
            The Chu-Liu tree of binary feature dependencies in the GramBank data.
        </small>
    </div>
</div>
<div class="span7">
    <p>

The strength of the functional dependency between two features F1 and F2 is defined as H(F2)/MI(F1, F2), over all languages for which both features are defined. H(X) is the Shannon entropy of the value distribution of the feature X across languages. MI(X, Y) = H(X)+H(Y)-H(X,Y) is the mutual information between X and Y. To hide circular and epiphenomenal dependencies the maximum spanning tree of the dependency graph is computed using the Chu-Liu algorithm. A dependency is called primary if it remains in the Chu-Liu and epiphenomenal otherwise. For more information, see:
<blockquote>
Hammarstr&ouml;m, Harald &amp; Loretta O'Connor. (2013) Dependency Sensitive Typological Distance. In Lars Borin &amp; Anju Saxena (eds.), Approaches to measuring linguistic differences, 337-360. Berlin: Mouton.
</blockquote>
</p>

</div>


${ctx.render()}
