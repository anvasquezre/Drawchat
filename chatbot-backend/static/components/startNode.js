const nodeName = "startNode";

const component = `
<div>
  <div class="title-box start" ><i class="fas fa-play-circle"></i>Start node</div>
  <div class="box">
    <p>Enter Text to display</p>
    <textarea df-text></textarea>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
<i class="fas fa-play-circle"></i><span> Start Node!</span>
<div id="description_start" style="display: none;">
    <p>chat starts here</p>
</div>
</div>`
;

export const initStartNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById("description_start");

    // Get a reference to the element you want to click on
    var element = document.querySelector(`div.drag-drawflow[data-node="${nodeName}"]`);

    // Add a click event listener to the element
    element.addEventListener("click", function () {
        // Toggle the display of the description div
        if (descriptionDiv.style.display === "none") {
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
};

export const addStartNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { text: "" },
    component
  );
};
